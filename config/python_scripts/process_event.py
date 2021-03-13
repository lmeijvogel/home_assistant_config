MAIN_SWITCH_NODE_ID = 10
KITCHEN_BUTTON_NODE_ID = 11

def main():
    logger.warning("%s", data)
    node_id = data.get("node_id", "none")
    scene_value_id = data.get("scene_value_id", "none")

    logger.debug("node_id: %s, scene_value_id: %s", node_id, scene_value_id)

    if scene_value_id == 0:
        return

    current_scene = hass.states.get("input_text.current_scene").state
    next_scene = get_next_scene(get_time_description, current_scene, node_id, scene_value_id)

    logger.info("Switch press: Switching from scene '%s' to '%s'", current_scene, next_scene)

    hass.services.call("scene", "turn_on", { "entity_id": next_scene }, False)
    hass.states.set("input_text.current_scene", next_scene)

def get_next_scene(time_description, current_scene, node_id, scene_value_id):
    if node_id == MAIN_SWITCH_NODE_ID:
        next_scene = get_next_scene_for_main_button(get_time_description(), scene_value_id, current_scene)
    elif node_id == KITCHEN_BUTTON_NODE_ID:
        next_scene = get_next_scene_for_kitchen_button(get_time_description(), scene_value_id, current_scene)

    if next_scene == None:
        logger.warning("Could not determine next scene from node '%s', scene_value_id '%s', current_scene '%s'", node_id, scene_value_id, current_scene);

        next_scene = current_scene

    return next_scene


def get_next_scene_for_main_button(time_description, scene_value_id, current_scene):
    button_actions = {
            10: "on",
            11: "off",
            14: "double_on"
    }
    button_action = button_actions.get(scene_value_id)
    transitions = { }

    default_scene = None
    if button_action == "off":
        default_scene = "scene.living_room_off"
    elif button_action == "on":
        if time_description == "night":
            default_scene = "scene.night"
        elif time_description == "morning":
            default_scene = "scene.morning"
        elif time_description == "evening":
            transitions = {
                "scene.evening": "scene.dimmed",
                "scene.dimmed": "scene.evening"
            }

            default_scene = "scene.evening"
    elif button_action == "double_on":
        default_scene = "scene.living_room_full"

    return transitions.get(current_scene, default_scene)

def get_next_scene_for_kitchen_button(time_description, scene_value_id, current_scene):
    if scene_value_id != 4:
        return

    transitions = { }

    off_scene = "scene.living_room_off"

    # Not interpolated for more flexibility later on
    if time_description == "night":
        on_scene = "scene.night"
    elif time_description == "morning":
        on_scene = "scene.morning"
    elif time_description == "evening":
        on_scene = "scene.evening"

    if current_scene == off_scene:
        return on_scene
    else:
        return off_scene

def get_time_description():
    time = datetime.datetime.now().time()

    if time < datetime.time(6, 0):
        return "night"
    elif time < datetime.time(14, 0):
        return "morning"
    elif time < datetime.time(23):
        return "evening"
    else:
        return "night"

main()
