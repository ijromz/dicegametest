import random

# ----------------------< Game rules constants  >-----------------------------------------------------------------------
# Rules can be parametrized by this globals constants
#
# Standard Farkle rules :
#  5 dices with 6 faces
#  1 & 5 are scoring
#  1 is scoring 100 pts
#  5 is scoring 50 pts
#
#  Bonus for 3 dices with the same value
#   3 ace is scoring 1000 pts
#   3 time the same dice value is scoring 100 pts x the dice value

class Algo:
  def __init__(self):
    self.NB_DICE_SIDE = 6  # Nb of side of the Dices
    self.SCORING_DICE_VALUE = [1, 5]  # list_value of the side values of the dice who trigger a standard score
    self.SCORING_MULTIPLIER = [100, 50]  # list_value of multiplier for standard score

    self.THRESHOLD_BONUS = 3  # Threshold of the triggering for bonus in term of occurrence of the same slide value
    self.STD_BONUS_MULTIPLIER = 100  # Standard multiplier for bonus
    self.ACE_BONUS_MULTIPLIER = 1000  # Special multiplier for aces bonus

    self.DEFAULT_DICES_NB = 5  # Number of dices by default in the set

    self.NUMBER_OF_TURNS = 3


  def roll_dice_set(self, nb_dice_to_roll):
      """ Generate the occurrence list of dice value for nb_dice_to_roll throw

          :parameters     nb_dice_to_roll         the number of dice to throw

          :return:        occurrence list of dice value
      """

      dice_value_occurrence = [0] * self.NB_DICE_SIDE
      dice_index = 0
      while dice_index < nb_dice_to_roll:
          dice_value = random.randint(1, self.NB_DICE_SIDE)
          dice_value_occurrence[dice_value - 1] += 1
          dice_index += 1

      return dice_value_occurrence


  def analyse_bonus_score(self, dice_value_occurrence):
      """ Compute the score for bonus rules and update occurrence list

          :parameters     dice_value_occurrence       occurrence list of dice value

          :return:        a dictionary with
                          - 'score'                   the score from bonus rules
                          - 'scoring_dice'            occurrence list of scoring dice value
                          - 'non_scoring_dice'        occurrence list of non scoring dice value
      """
      scoring_dice_value_occurrence = [0] * self.NB_DICE_SIDE

      bonus_score = 0
      side_value_index = 0
      while side_value_index < len(dice_value_occurrence):

          side_value_occurrence = dice_value_occurrence[side_value_index]

          nb_of_bonus = side_value_occurrence // self.THRESHOLD_BONUS
          if nb_of_bonus > 0:
              if side_value_index == 0:
                  bonus_multiplier = self.ACE_BONUS_MULTIPLIER
              else:
                  bonus_multiplier = self.STD_BONUS_MULTIPLIER
              bonus_score += nb_of_bonus * bonus_multiplier * (side_value_index + 1)

              # update the occurrence list after bonus rules for scoring dices and non scoring dices
              dice_value_occurrence[side_value_index] %= self.THRESHOLD_BONUS
              scoring_dice_value_occurrence[side_value_index] = nb_of_bonus * self.THRESHOLD_BONUS

          side_value_index += 1

      return {'score': bonus_score,
              'scoring_dice': scoring_dice_value_occurrence,
              'non_scoring_dice': dice_value_occurrence}


  def analyse_standard_score(self, dice_value_occurrence):
      """ Compute the score for standard rules and update occurrence list

          :warning :      occurrence list of dice value should be cleaned from potential bonus
                          call analyse_bonus_score() first

          :parameters     dice_value_occurrence       occurrence list of dice value

          :return:        a dictionary with
                          - 'score'                   the score from standard rules
                          - 'scoring_dice'            occurrence list of scoring dice value
                          - 'non_scoring_dice'        occurrence list of non scoring dice value
      """
      scoring_dice_value_occurrence = [0] * self.NB_DICE_SIDE

      standard_score = 0
      scoring_dice_value_index = 0
      while scoring_dice_value_index < len(self.SCORING_DICE_VALUE):
          scoring_value = self.SCORING_DICE_VALUE[scoring_dice_value_index]
          scoring_multiplier = self.SCORING_MULTIPLIER[scoring_dice_value_index]

          standard_score += dice_value_occurrence[scoring_value - 1] * scoring_multiplier

          # update the occurrence list after standard rules for scoring dices and non scoring dices
          scoring_dice_value_occurrence[scoring_value - 1] = dice_value_occurrence[scoring_value - 1]
          dice_value_occurrence[scoring_value - 1] = 0

          scoring_dice_value_index += 1

      return {'score': standard_score,
              'scoring_dice': scoring_dice_value_occurrence,
              'non_scoring_dice': dice_value_occurrence}


  def analyse_score(self, dice_value_occurrence):
      """ Compute the score for standard and bonus rules, update occurrence list

          :parameters     dice_value_occurrence       occurrence list of dice value

          :return:        a dictionary with
                          - 'score'                   the score from standard rules
                          - 'scoring_dice'            occurrence list of scoring dice value
                          - 'non_scoring_dice'        occurrence list of non scoring dice value
      """

      analyse_score_bonus = self.analyse_bonus_score(dice_value_occurrence)
      score_bonus = analyse_score_bonus['score']
      scoring_dice_from_bonus = analyse_score_bonus['scoring_dice']
      non_scoring_dice_from_bonus = analyse_score_bonus['non_scoring_dice']

      analyse_score_std = self.analyse_standard_score(non_scoring_dice_from_bonus)
      score_std = analyse_score_std['score']
      scoring_dice_from_std = analyse_score_std['scoring_dice']
      non_scoring_dice_from_std = analyse_score_std['non_scoring_dice']

      # the occurrence list of scoring dice value is the sum from scoring dice by bonus and standard rules
      scoring_dice_value_occurrence = [0] * self.NB_DICE_SIDE
      side_value_index = 0
      while side_value_index < self.NB_DICE_SIDE:
          scoring_dice_value_occurrence[side_value_index] = scoring_dice_from_bonus[side_value_index] + \
                                                            scoring_dice_from_std[side_value_index]
          side_value_index += 1

      return {'score': score_std + score_bonus,
              'scoring_dice': scoring_dice_value_occurrence,
              'non_scoring_dice': non_scoring_dice_from_std}


  def game_turn(self, is_interactive=True):
      """ Handle a full player turn

          :parameters     current_player      dictionary of player information
                                              - 'name'
                                              - 'score'
                                              - 'lost_score'
                                              - 'nb_of_roll'
                                              - 'nb_of_turn'
                                              - 'nb_of_scoring_turn'
                                              - 'nb_of_non_scoring_turn'
                                              - 'nb_of_full_roll'

                          is_interactive      boolean for game mode
                                              - True -> interactive game mode
                                              - False -> random choice for game simulation

          :return:        updated dictionary of player information after a game turn
      """

      # turn start with the full set of dices
      remaining_dice_to_roll = self.DEFAULT_DICES_NB
      roll_again = True

      turn_score = 0
      while roll_again:
          # generate the dice roll and compute the scoring
          dice_value_occurrence = self.roll_dice_set(remaining_dice_to_roll)
          roll_score = self.analyse_score(dice_value_occurrence)
          remaining_dice_to_roll = sum(roll_score['non_scoring_dice'])

          if roll_score['score'] == 0:
              # lost roll

              print('\n-->', 'got zero point ', turn_score, 'lost points\n')

              roll_again = False
              turn_score = 0
          else:
              # scoring roll

              turn_score += roll_score['score']

              # In case of scoring roll and no remaining dice to roll the player can roll again the full set of dices
              if remaining_dice_to_roll == 0:
                  remaining_dice_to_roll = self.DEFAULT_DICES_NB
                  print('-->Full Roll')

              print('Roll Score=', roll_score['score'], 'potential turn score=', turn_score, 'remaining dice=',
                    remaining_dice_to_roll)

              # choice to roll again or stop and take roll score
              if is_interactive:
                  # interactive decision for real game
                  stop_turn = input("Do you want to roll this dice ? [y/n] ") == "n"
              else:
                  # random decision for game simulation (50/50)
                  stop_turn = (random.randint(1, 100) % 2) == 0

              if stop_turn:
                  # stop turn and take roll score

                  print('\n-->', 'Scoring turn with', turn_score, 'points\n')

                  roll_again = False

      return turn_score

  def multiplayerGame(self, players):
      turn_number = 1
      NUMBER_OF_PLAYERS = len(players)
      score_board = [0] * NUMBER_OF_PLAYERS
      while turn_number <= self.NUMBER_OF_TURNS :
          print(turn_number)
          player_id = 0
          while player_id < NUMBER_OF_PLAYERS :
              print(players[player_id] + "'s turn")
              turn_score = self.game_turn(True)
              score_board[player_id] += turn_score
              print(score_board)
              player_id += 1
          turn_number += 1
