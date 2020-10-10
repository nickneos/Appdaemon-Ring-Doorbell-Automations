# Ring Doorbell Automations App
Trigger automations when a Ring Doorbell button is pressed:

* Play alert sound on media device (eg. google home)
* Courtesy light (eg. turn of front porch light when doorbell pressed)
* Flash lights in the house
* TTS voice prompt (eg. google home)

## Configuration

### Example config

```yaml
ring_automations:
  module: ring_automations
  class: Doorbell
  doorbell: binary_sensor.front_door_ding
  courtesy_light: 
    light: light.front_porch
    timer: 180
  alert_sound:
    media_player: media_player.google_home_main
    media_content: "https://www.myinstants.com/media/sounds/dj-airhorn-sound-effect-kingbeatz_1.mp3"
  flash_lights:
    - light.hallway
    - light.kitchen
    - light.living_room
  tts:
    media_player: media_player.google_home_main
    message: "There's someone at the door."
```


### Main Config options

| Variable       | Type       | Required | Description                                                                                                      |
| -------------- | ---------- | -------- | ---------------------------------------------------------------------------------------------------------------- |
| module         | string     | Required | Set to `ring_automations`                                                                                        |
| class          | string     | Required | Set to `Doorbell`                                                                                                |
| doorbell       | string     | Required | `entity_id` of the ring doorbell                                                                                 |
| courtesy_light | dictionary | Optional | Specifiy settings for a courtesy light to turn on when doorbell is pressed (eg. front porch light). Refer below. |
| alert_sound    | dictionary | Optional | Specifiy an audio file to play on a media player when doorbell is pressed. Refer below.                          |
| flash_lights   | list       | Optional | List of lights to flash in the house when doorbell is pressed.                                                   |
| tts            | dictionary | Optional | Specifiy a Text to Speech message to play on a media_player. Refer below.                                        |

### courtesy_light

| Variable | Type   | Required | Description                                             |
| -------- | ------ | -------- | ------------------------------------------------------- |
| light    | string | Required | `entity_id` of light                                    |
| timer    | int    | Required | Number of seconds for light to remain on. Default: `60` |

### alert_sound

| Variable      | Type   | Required | Description                                                                                                   |
| ------------- | ------ | -------- | ------------------------------------------------------------------------------------------------------------- |
| media_player  | string | Required | `entity_id` of media player                                                                                   |
| media_content | string | Required | URL of audio file. Default: `https://www.myinstants.com/media/sounds/dj-airhorn-sound-effect-kingbeatz_1.mp3` |

### tts

| Variable     | Type   | Required | Description                                           |
| ------------ | ------ | -------- | ----------------------------------------------------- |
| media_player | string | Required | `entity_id` of media player                           |
| timer        | int    | Required | TTS message. Default: `"There's someone at the door"` |
