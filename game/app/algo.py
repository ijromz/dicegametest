import random

NB_DICE_SIDE = 6  # Nb of side of the Dices
SCORING_DICE_VALUE = [1, 5]  # list_value of the side values of the dice who trigger a standard score
SCORING_MULTIPLIER = [100, 50]  # list_value of multiplier for standard score

THRESHOLD_BONUS = 3  # Threshold of the triggering for bonus in term of occurrence of the same slide value
STD_BONUS_MULTIPLIER = 100  # Standard multiplier for bonus
ACE_BONUS_MULTIPLIER = 1000  # Special multiplier for aces bonus

DEFAULT_DICES_NB = 5  # Number of dices by default in the set
class Algo:
  def roll_dice_set(nb_dice_to_roll):
    dice_value_occurrence = [0] * NB_DICE_SIDE
    dice_index = 0
    while dice_index < nb_dice_to_roll:
        dice_value = random.randint(1, NB_DICE_SIDE)
        dice_value_occurrence[dice_value - 1] += 1
        dice_index += 1

    return dice_value_occurrence

  a = roll_dice_set(5)
