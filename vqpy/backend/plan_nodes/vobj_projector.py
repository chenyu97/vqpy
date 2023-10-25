from typing import Any, Callable, Dict
from vqpy.backend.operator.vobj_projector_new import VObjProjector
from vqpy.backend.plan_nodes.base import AbstractPlanNode
from vqpy.frontend.query import QueryBase
from vqpy.frontend.vobj.predicates import Predicate
from vqpy.frontend.vobj.property import Property, BuiltInProperty
from vqpy.backend.plan_nodes.vobj_filter import create_vobj_filter_node_pred


class ProjectionField:
    def __init__(
        self,
        field_name: str,
        field_func: Callable[[Dict], Any],
        dependent_fields: Dict[str, int],
        is_stateful: bool,
    ):
        self.field_name = field_name
        self.field_func = field_func
        self.dependent_fields = dependent_fields
        self.is_stateful = is_stateful


class ProjectorNode(AbstractPlanNode):
    def __init__(
        self,
        class_name: str,
        projection_field: ProjectionField,
        filter_index: int,
    ):
        self.class_name = class_name
        self.projection_field = projection_field
        self.filter_index = filter_index
        super().__init__()

    def to_operator(self, launch_args: dict):
        return VObjProjector(
            prev=self.prev.to_operator(launch_args),
            property_name=self.projection_field.field_name,
            property_func=self.projection_field.field_func,
            dependencies=self.projection_field.dependent_fields,
            is_stateful=self.projection_field.is_stateful,
            class_name=self.class_name,
            filter_index=self.filter_index,
        )

    def __str__(self):
        return (
            f"ProjectorNode(class_name={self.class_name}, \n"
            f"\tproperty_name={self.projection_field.field_name}, \n"
            f"\tfilter_index={self.filter_index}), \n"
            f"\tdependencies={self.projection_field.dependent_fields}),\n"
            f"\tis_stateful={self.projection_field.is_stateful}), \n"
            f"\tprev={self.prev.__class__.__name__}), \n"
            f"\text={self.next.__class__.__name__})"
        )


def create_pre_filter_projector(query_obj: QueryBase, input_node):
    frame_constraints = query_obj.frame_constraint()

    node = input_node

    vobj_properties_map = dict()

    if isinstance(frame_constraints, Predicate):
        vobjs = frame_constraints.get_vobjs()
        assert len(vobjs) == 1, "Only support one vobj in the predicate"
        vobj = list(vobjs)[0]
        vobj_properties = frame_constraints.get_vobj_properties()
        for p in vobj_properties:
            projector_node = ProjectorNode(
                class_name=vobj.class_name,
                projection_field=ProjectionField(
                    field_name=p.name,
                    field_func=p,
                    dependent_fields=p.inputs,
                    is_stateful=p.stateful,
                ),
                filter_index=0,
            )
            node = node.set_next(projector_node)
        vobj_properties_map[vobj] = vobj_properties

    return node, vobj_properties_map


def split_predicate(predicate):
    from vqpy.frontend.vobj.predicates import And
    if isinstance(predicate, And):
        return split_predicate(predicate.left_pred) + split_predicate(
            predicate.right_pred
        )
    else:
        return [predicate]


def get_prop_pred_map(predicates):
    # traverse the predicates and get the map from property to predicates
    # if the predicate is a comparison predicate with one property,
    # then return the map from the property to predicates that use the property
    prop_pred_map = dict()
    rest_predicates = []
    for predicate in predicates:
        if predicate.is_comparison():
            prop_names = predicate.get_self_vobj_property_names()
            if len(prop_names) == 1:
                prop_name = list(prop_names)[0]
                prop_pred_map[prop_name] = prop_pred_map.get(prop_name, []) + [
                    predicate
                ]
            else:
                rest_predicates.append(predicate)
        else:
            rest_predicates.append(predicate)
    return prop_pred_map, rest_predicates


def create_projector_adjacent_to_filter(query_obj: QueryBase, input_node):
    frame_constraints = query_obj.frame_constraint()

    node = input_node

    vobj_properties_map = dict()

    predicates = split_predicate(frame_constraints)
    prop_pred_map, rest_predicates = get_prop_pred_map(predicates)

    if isinstance(frame_constraints, Predicate):
        vobjs = frame_constraints.get_vobjs()
        assert len(vobjs) == 1, "Only support one vobj in the predicate"
        vobj = list(vobjs)[0]
        vobj_properties = frame_constraints.get_vobj_properties()
        for p in vobj_properties:
            projector_node = ProjectorNode(
                class_name=vobj.class_name,
                projection_field=ProjectionField(
                    field_name=p.name,
                    field_func=p,
                    dependent_fields=p.inputs,
                    is_stateful=p.stateful,
                ),
                filter_index=0,
            )
            node = node.set_next(projector_node)

            # add filter node adjacent to the projector node
            # if the property is used in a comparison predicate
            if p.name in prop_pred_map:
                for predicate in prop_pred_map[p.name]:
                    filter_node = create_vobj_filter_node_pred(
                        predicate, node
                    )
                    node = projector_node.set_next(filter_node)

            # add filter node for the rest predicates
        for predicate in rest_predicates:
            filter_node = create_vobj_filter_node_pred(
                predicate, node
            )
            node = node.set_next(filter_node)

        vobj_properties_map[vobj] = vobj_properties

    return node, vobj_properties_map


def create_frame_output_projector(
    query_vobj: QueryBase, input_node, vobj_properties_map: dict
):
    existing_vobj_properties = vobj_properties_map.copy()
    frame_output = query_vobj.frame_output()
    if isinstance(frame_output, Property):
        frame_output = [frame_output]
    for prop in frame_output:
        vobj = prop.get_vobjs()
        assert len(vobj) == 1, "Only support one vobj for vobj_property."
        vobj = list(vobj)[0]
        existing_properties = existing_vobj_properties[vobj]
        if not isinstance(prop, BuiltInProperty):
            if all([prop.func != ep.func for ep in existing_properties]):
                projector_node = ProjectorNode(
                    class_name=vobj.class_name,
                    projection_field=ProjectionField(
                        field_name=prop.name,
                        field_func=prop,
                        dependent_fields=prop.inputs,
                        is_stateful=prop.stateful,
                    ),
                    filter_index=0,
                )
                input_node = input_node.set_next(projector_node)
                existing_properties.append(prop)
    return input_node
