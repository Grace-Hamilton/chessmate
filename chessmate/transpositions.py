""" Functions related to hash_tableing and transposition tables """
import random
from typing import Dict, List

import chess  # type: ignore

from analysis import StandardEvaluation
from constants.misc import PIECE_INDEXING
from utils import get_piece_at


def zobrist_hash_function(board: chess.Board, hash_table: List) -> int:
    """
    Hashes board according to Zobrist hash schema

    Args:
        board (chess.Board): boardstate
        hash_table (List): randomly generated hash table
    Returns:
        (int): hashed board
    """
    _hash = 0
    for square in chess.SQUARES:
        piece = get_piece_at(board=board, position=square)
        # If piece on square, hash piece based off piece identity and position
        if piece:
            piece_idx = PIECE_INDEXING[piece]
            rank, _file = chess.square_rank(square), chess.square_file(square)
            # Bitwise XOR on _hash
            _hash ^= hash_table[rank][_file][piece_idx]

    return _hash


class TranspositionTable:
    """
    Base class for transposition tables

    Attributes:
        hash_function (Callable): function that hashed board to int
        hash_table (List): hash table to feed into hash function.
            Randomly generated by default
        evaluation_function: function to evaluate boardstate
        stored_values (Dict[int, int]): table to store results

    Methods:
        hash_current_board (chess.Board): hashes and evaluates
            board based off hash_function and evaluation_function
            respectively, store hashed board eval in stored_values
    """

    def __init__(self, hash_function):
        self.hash_function = hash_function
        self._hash_table = [
            [
                [random.randint(1, 2 ** 64 - 1) for i in range(12)]
                for j in range(8)
            ]
            for k in range(8)
        ]
        self.evaluation_function = StandardEvaluation
        self.stored_values: Dict[int, int] = {}

    def __len__(self):
        return len(self.stored_values)

    def __contains__(self, hash_str: str) -> bool:
        return hash_str in self.stored_values

    @property
    def hash_table(self) -> List:
        """ Getter for hash_table """
        return self._hash_table

    @hash_table.setter
    def hash_table(self, new_hash_table: List):
        """
        Setter for hash_table

        Args:
            new_hash_table (List)
        """
        self._hash_table = new_hash_table

    def hash_current_board(self, board: chess.Board) -> None:
        """
        Adds hashed boardstate to stored_values with evaluation

        Args:
            board (chess.Board): board state
        """
        hash_ = self.hash_function(board, self._hash_table)
        evaluation = self.evaluation_function().evaluate(board)
        self.stored_values[hash_] = evaluation
