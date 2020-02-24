from world import World, DailyHistory

import argparse
import glob
import os
import pickle
from PIL import Image

def save_gif(file_pattern, gif_name, delete_imgs=False, frame_duration=100):
  """Using Pillow image library to change alphabetical png files into gifs.

  Arguments:
    file_pattern: string; File pattern of the images to use.
    gif_name: string; Filename to save ('.gif' will be appended automatically).
  """
  frames = []
  directory = "/mnt/c/Users/dmcin/Desktop/projects/simulations/tmp_plots/"
  imgs = glob.glob(directory + file_pattern)

  # Open the images.
  for i in sorted(imgs):
      frames.append(Image.open(i))

  # Save into looping gif file.
  frames[0].save(directory + gif_name + '.gif',
                 format='GIF',
                 append_images=frames[1:],
                 save_all=True,
                 duration=frame_duration, loop=0)
  if delete_imgs:
    [os.remove(file) for file in imgs]

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--world_pkl", "-wp", help="pickled world file")
  args = parser.parse_args()
  directory = "/mnt/c/Users/dmcin/Desktop/projects/simulations/tmp_plots/"
  if args.world_pkl:
    # Reuse old world.
    with open(directory + args.world_pkl, "rb") as f:
      my_world=pickle.load(f)
  else:
    # Create a small world, with lots of food and 1 creature
    print("Creating World...")
    my_world = World(50, 0.07, 1, reproduction_mutation_chance=0)
    # Overwrite location to start the creature near the middle of the map.
    my_world.creatures[0].location = [20, 20]

  for i in range(40):
    my_world.pass_day(40,
                      plot_steps=(True if i < 5 else False))
    if i < 21:
      my_world.show_me(save_plot=True)
    print("days_passed: ", my_world.days_passed,
          "; creatures: ", len(my_world.creatures))
  my_world.plot_history(save_plot=True)
  save_gif("*_t_*.png", "the_first_days", delete_imgs=True, frame_duration=100)
  save_gif("world_2*.png", "each_day", delete_imgs=True, frame_duration=800)

  with open(directory+"my_world.pkl", "wb") as f:
    pickle.dump(my_world, f)

if __name__ == "__main__":
  main()