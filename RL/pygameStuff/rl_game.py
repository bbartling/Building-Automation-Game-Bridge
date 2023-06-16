# Importing necessary libraries
import pygame
import os
import gym
import pygame
import numpy as np
from gym import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy
import sys

# Mario game class
class MarioGame:
    def __init__(self):
        pygame.init()  # Initialize all imported pygame modules

        # Set up the game window
        self.screen = pygame.display.set_mode((800, 600))  # Set the size of the window
        pygame.display.set_caption("Mario Level")  # Set the title of the window
        self.clock = pygame.time.Clock()  # Create an object to help track time

        # Load and set up the Mario image
        self.mario_image = pygame.image.load("mario.png")  # Load the Mario image
        self.mario_rect = pygame.Rect(100, 500, 40, 40)  # Create a rectangle for Mario
        self.mario_image = pygame.transform.scale(self.mario_image, (40, 40))  # Scale the image to fit the rectangle

        # Load and set up the question box image
        self.question_box_image = pygame.image.load("question_box.png")  # Load the question box image
        self.question_box_rect = pygame.Rect(150, 50, 40, 40)  # Create a rectangle for the question box
        self.question_box_image = pygame.transform.scale(self.question_box_image, (40, 40))  # Scale the image to fit the rectangle
        self.question_box_active = True  # The question box is initially active

        # Create platforms for Mario to jump on
        self.platforms = [
            pygame.Rect(50, 500, 200, 10),
            pygame.Rect(300, 450, 200, 10),
            pygame.Rect(150, 175, 200, 10),
            pygame.Rect(210, 400, 200, 10),
            pygame.Rect(260, 300, 200, 10),
        ]

        # Physics parameters for Mario's movement
        self.falling = True  # Mario starts falling
        self.vertical_velocity = 0.0  # Initial vertical velocity is 0
        self.jump_power = 14.0  # Power of Mario's jump
        self.gravity = 0.6  # Gravitational pull

    def reset(self):
        # Reset the game state to the beginning
        self.mario_rect = pygame.Rect(100, 500, 40, 40)
        self.question_box_active = True
        self.vertical_velocity = 0.0
        self.falling = True
        # Return the initial state of the game
        return np.array([self.mario_rect.center[0], self.mario_rect.center[1], self.vertical_velocity, int(self.question_box_active)])

    def get_state(self):
        # Return the current state of the game
        return self.mario_rect.center, self.vertical_velocity, self.question_box_active

    def step(self, action):
        # This function executes the action in the game and returns the new state, reward and done
        speed = 5  # Mario's speed

        # Move Mario according to the action
        if action == 0:  # Move Left
            self.mario_rect.move_ip(-speed, 0)
        elif action == 1:  # Move Right
            self.mario_rect.move_ip(speed, 0)
        elif action == 2 and not self.falling:  # Jump
            self.vertical_velocity -= self.jump_power
            self.falling = True

        # Apply gravity and move Mario
        self.vertical_velocity += self.gravity
        self.mario_rect.move_ip(0, self.vertical_velocity)

        # Handle collisions with platforms
        for platform in self.platforms:
            if self.mario_rect.colliderect(platform):
                if self.vertical_velocity > 0:  # Mario is falling
                    self.mario_rect.bottom = platform.top  # Stop Mario at the platform
                    self.falling = False
                    self.vertical_velocity = 0.0
                elif self.vertical_velocity < 0:  # Mario is jumping
                    self.mario_rect.top = platform.bottom  # Stop Mario below the platform
                    self.vertical_velocity = 0.0
                    
        # Check if Mario has fallen off the platform
        if self.mario_rect.top > self.screen.get_height():
            done = True  # The game is over
        else:
            # Check if Mario has reached the question box
            done = False
            if self.mario_rect.colliderect(self.question_box_rect) and self.question_box_active:
                done = True  # The game is over

        # Return new state, reward, and whether the game is over
        return np.array([self.mario_rect.center[0], self.mario_rect.center[1], self.vertical_velocity, int(self.question_box_active)]), -1, done

    def render(self):
        # Draw everything on the screen
        self.screen.fill((255, 255, 255))  # Fill the screen with white

        # Draw the platforms
        for platform in self.platforms:
            pygame.draw.rect(self.screen, (0, 255, 0), platform)  # Draw a green rectangle for each platform

        # Draw the question box if it is active
        if self.question_box_active:
            self.screen.blit(self.question_box_image, self.question_box_rect)  # Draw the question box image

        # Draw Mario
        self.screen.blit(self.mario_image, self.mario_rect)  # Draw the Mario image

        pygame.display.flip()  # Update the display

        self.clock.tick(60)  # Limit the game to 60 frames per second


# Environment for the Mario game
class MarioLevelEnv(gym.Env):
    def __init__(self):
        super(MarioLevelEnv, self).__init__()

        # Define action and observation space
        self.action_space = spaces.Discrete(3)  # Mario can do 3 things: move left, move right, jump
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(4,), dtype=np.float32)  # The observation is a 4-dimensional vector

        self.game = MarioGame()  # Create a new Mario game

    def step(self, action):
        # Execute the action and get the new state, reward and done
        obs, reward, done = self.game.step(action)

        # Render the game
        self.game.render()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit the game
                sys.exit()  # Exit the program

        return obs, reward, done, {}  # Return the new state, reward, done and extra information

    def reset(self):
        # Reset the game
        return self.game.reset()  # Return the initial state


def create_environment():
    # Create and monitor the environment
    env = MarioLevelEnv()  # Create a new environment with the Mario game
    env = Monitor(env, log_dir)  # Monitor the environment for logging
    return env

log_dir = "/tmp/gym/"  # Directory for logs
os.makedirs(log_dir, exist_ok=True)  # Make sure the directory exists

env = DummyVecEnv([lambda: create_environment()])  # Create a vectorized environment

model = PPO('MlpPolicy', env, verbose=1, learning_rate=0.0003, n_steps=500)  # Create the PPO agent
model.learn(total_timesteps=500000)  # Train the agent



print("Hit enter to continue...")
input()


mean_reward, _ = evaluate_policy(model, env, n_eval_episodes=10)  # Evaluate the policy
obs = env.reset()  # Reset the environment and get the initial observation

# After training, let's watch our agent play the game
for _ in range(10):  # Play 10 full games
    obs = env.reset()  # Reset the environment at the start of each game
    done = False
    while not done:  # Keep going until the game is done
        action, _ = model.predict(obs, deterministic=True)  # The agent selects an action
        obs, _, done, _ = env.step(action)  # Perform the action in the environment
        env.render()  # Render the current state of the environment
