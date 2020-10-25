from profiling import time_profiling, memory_profiling


class ActionSystem:

    def get_actions(self, ai_components, percepts, actions_components,
                    score_components, label_components, random_generator):
        actions = {}
        for actor_id, ai in ai_components.items():
            try:
                percept = percepts[actor_id]
            except KeyError:
                percept = {}

            do_time_profiling = (actor_id in label_components
                                 and time_profiling.started)
            do_memory_profiling = (actor_id in label_components
                                   and memory_profiling.started)
            if do_time_profiling:
                time_profiling.set_context(label_components[actor_id])
            if do_memory_profiling:
                memory_profiling.set_context(label_components[actor_id])

            if hasattr(ai, "update_state_percept"):
                ai.update_state_percept(percept)
            action = ai.next_action(percept, random_generator)
            if hasattr(ai, "update_state_action"):
                ai.update_state_action(action)

            if do_time_profiling:
                time_profiling.unset_context(label_components[actor_id])
            if do_memory_profiling:
                memory_profiling.unset_context(label_components[actor_id])

            action_type = action.action_type
            if action_type == "none":
                continue
            # Don't perform actions we're not allowed to
            if (actor_id not in actions_components
                    or action_type not in
                    actions_components[actor_id]):
                continue
            # Apply cost of action, if any
            if (actions_components[actor_id][action_type].cost
                    is not None
                    and actor_id in score_components):
                cost = actions_components[actor_id][action_type].cost
                score_components[actor_id] -= cost
            actions[actor_id] = action
        return actions
