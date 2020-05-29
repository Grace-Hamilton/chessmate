""" Test suite for assortment of helper functions """
import sys

import chess
import chess.pgn
import pytest

from analysis import StandardEvaluation
from engines import ScholarsMate
from simulations import ChessPlayground
from constants import *
from utils import *

sys.path.append("..")


@pytest.fixture
def starting_board():
    """
    Set ups empty board for each test

    Returns:
        (chess.Board)
    """
    game = chess.pgn.Game()
    board = game.board()
    return board


@pytest.fixture
def in_progress_board():
    """
    Set ups board of an in progress game

    Returns:
        (chess.Board)
    """
    in_progress_fen = (
        "2kr1bnr/2ppqppp/p7/2p1p3/" "3PP3/2N2N2/PPP2PPP/R1BQK2R w KQk - 0 1"
    )
    board = chess.Board(fen=in_progress_fen)
    return board


@pytest.fixture
def setup_playground():
    """
    Sets up test playground with 3 games played

    Returns:
            (ChessPlaygound)
    """
    playground = ChessPlayground(ScholarsMate(), ScholarsMate())
    playground.play_multiple_games(3)
    return playground


@pytest.fixture
def setup_piece_tables():
    """ Sets ups all defined piece tables """
    return [
        piece_values.PAWN_PIECE_TABLE_CONVENTIONAL,
        piece_values.KNIGHT_PIECE_TABLE_CONVENTIONAL,
        piece_values.BISHOP_PIECE_TABLE_CONVENTIONAL,
        piece_values.ROOK_PIECE_TABLE_CONVENTIONAL,
        piece_values.QUEEN_PIECE_TABLE_CONVENTIONAL,
        piece_values.ROOK_PIECE_TABLE_CONVENTIONAL,
    ]


def test_get_square_at_position_lowercase_str():
    """ Tests that get_square_at_position return proper square
    for lowercase inputs """
    assert get_square_at_position("a2") == chess.A2


def test_get_square_at_position_uppercase_str():
    """ Tests that get_square_at_position return proper square
    for uppercase inputs """
    assert get_square_at_position("A2") == chess.A2


def test_get_square_at_position_square_input():
    """ Tests that get_square_at_position return proper square
    for chess.square inputs """
    assert get_square_at_position(chess.A2) == chess.A2


def test_piece_at_function_on_starting_position(starting_board):
    """ Tests that piece_at function returns correct
    symbol of piece at square in starting position"""
    piece_at_rook_square = get_piece_at(starting_board, chess.A8)
    piece_at_king_square = get_piece_at(starting_board, "e1")
    piece_at_pawn_square = get_piece_at(starting_board, "e2")

    assert piece_at_rook_square == "r"
    assert piece_at_king_square == "K"
    assert piece_at_pawn_square == "P"


def test_piece_at_function_on_empty_square(starting_board):
    """ Tests that piece_at function returns False for
    empty squares """
    piece_at_empty_square = get_piece_at(starting_board, "C3")
    assert not piece_at_empty_square


def test_piece_at_function_on_inprogress_board(in_progress_board):
    """ Tests that piece at function returns
    value of piece at square in a game in progress"""
    piece_at_square_occupied_by_pawn = get_piece_at(in_progress_board, "e4")
    piece_at_square_occupied_by_queen = get_piece_at(
        in_progress_board, chess.E7
    )

    assert piece_at_square_occupied_by_pawn == "P"
    assert piece_at_square_occupied_by_queen == "q"


def test_piece_at_function_on_empty_square_inprogress_board(in_progress_board):
    """ Tests that piece at function returns False for empty square
    for a board that's not the starting board """
    piece_at_empty_square = get_piece_at(in_progress_board, "F1")
    assert not piece_at_empty_square


def test_display_pgn_text_no_errors(setup_playground):
    """ Tests that display_pgn_text runs in console w/o errors"""
    display_pgn_text(setup_playground.game_pgns[0])


def test_walkthrough_pgn_no_errors(setup_playground):
    """ Tests that walkthrough_pgn runs w/o errors. Note that since
    this function relies on IPython functionality, nothing will appear
    to happen """
    walkthrough_pgn(setup_playground.game_pgns[0])


def test_display_all_results_no_errors(setup_playground):
    """ Tests that display_all_results runs. Since this function
    displays in IPython console, having it run w/o errors is
    sufficient. """
    display_all_results(setup_playground.all_results)


def test_display_material_difference_no_errors(setup_playground):
    """ Tests that display_material_difference runs. Since this function
    displays in IPython console, having it run w/o errors is
    sufficient. """
    display_material_difference(setup_playground.all_material_differences, 0)
    display_material_difference(setup_playground.all_material_differences, 1)


def test_display_all_material_differences_no_errors(setup_playground):
    """ Tests that all_display_material_difference runs. Since this function
    displays in IPython console, having it run w/o errors is
    sufficient."""
    display_all_material_differences(setup_playground.all_material_differences)


def test_piece_tables(setup_piece_tables):
    """ Tests that piece tables are of correct shape (8x8 )"""
    for table in setup_piece_tables:
        assert table.shape == (8, 8)


def test_get_piece_value_from_table_white_square():
    """ Tests that get piece_value_from_table function returns
    correct values for white squares"""
    a1_pawn_value = get_piece_value_from_table(
        "P", chess.WHITE, "a1", piece_values.PIECE_TABLE_CONVENTIONAL
    )

    a2_pawn_value = get_piece_value_from_table(
        "P", chess.WHITE, "a2", piece_values.PIECE_TABLE_CONVENTIONAL
    )
    assert a1_pawn_value == 0.0
    assert a2_pawn_value == 0.5


def test_get_piece_value_from_table_black_square():
    """ Tests that get piece_value_from_table function returns
    correct values for black squares. Note that black tables are
    rotated 180 from white tables """
    c3_knight_value = get_piece_value_from_table(
        "N", chess.BLACK, "c3", piece_values.PIECE_TABLE_CONVENTIONAL
    )

    d4_knight_value = get_piece_value_from_table(
        "N", chess.BLACK, "d4", piece_values.PIECE_TABLE_CONVENTIONAL
    )
    assert c3_knight_value == 1.0
    assert d4_knight_value == 2.0
