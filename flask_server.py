import json
from pathlib import Path

from flask import Flask, request, render_template
from sb3_contrib import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker

from with_masking import SixthTakes, mask_fn

app = Flask(__name__)

model_path = Path("Training", "Models", "Maskable_PPO")

model = MaskablePPO.load(model_path, print_system_info=True)
masking_env = SixthTakes()
masking_env = ActionMasker(masking_env, mask_fn)


def observation_to_json(observation, players, done):
    player_dict = {}
    for player in players:
        player_dict[f"player_{player.id}"] = {"penalty_sum": int(player.penalty_sum)}
    to_json_dict = {
        "hand_cards": observation["hand_cards"].astype(int).tolist(),
        "piles": observation["piles"].astype(int).tolist(),
        "played_cards": observation["played_cards"].astype(int).tolist(),
        "player_dict": player_dict,
        "done": done
    }
    return json.dumps(to_json_dict, indent=4)


# masking_env.reset()
# current_observation = masking_env.get_obs()
# ai_action, _ = model.predict(current_observation)
#
# print("Stop")


@app.route("/make_action", methods=['POST'])
def make_action():
    global current_observation
    global model
    global masking_env
    move = json.loads(request.data)
    move["action"] = int(move["action"])
    # if move -1 -> start new game
    if move["action"] == -1:
        masking_env.reset()
        current_observation = masking_env.get_obs()
        return observation_to_json(current_observation, masking_env.players, masking_env.done)
    else:
        human_step = move["action"]
        ai_action, _ = model.predict(current_observation)
        masking_env.players[0].select_playing_card(ai_action)
        masking_env.players[1].select_playing_card(human_step)
        masking_env.play_round()
        current_observation = masking_env.get_obs()
        return observation_to_json(current_observation, masking_env.players, masking_env.done)


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", threaded=True, use_reloader=False)