from __future__ import annotations

from enum import Enum

from abc import ABC, abstractmethod
import re

from pymunk.vec2d import Vec2d
from colorama import Fore, Style, Back
from hashlib import sha256


class Engine:
    def __init__(self):
        self.board = []

        self.reset_board()

    def run(self):
        def get_position_input(text: str, options: [str] = None) -> Position:
            while True:
                description = input(f'{text} ({", ".join(options)}) ') if options is not None else input(text + ' ')
                if re.fullmatch('[A-H][1-8]', description):
                    if options is not None and description not in options:
                        continue
                    return Position.from_description(description)

        while True:
            self.print_board()
            a = get_position_input('Select a piece:')
            piece = self.get(a)

            moves = piece.get_possible_moves(self)

            piece.focused = True
            self.print_board(moves)
            piece.focused = False

            b = get_position_input('Select a resulting position:', [move.b.description for move in moves])
            move = Move(a, b)
            self.apply_move(move)

    def reset_board(self, white_up=True):
        if white_up:
            self.board = [
                Rook(Position.from_description('A8'), Color.White),
                Knight(Position.from_description('B8'), Color.White),
                Bishop(Position.from_description('C8'), Color.White),
                Queen(Position.from_description('D8'), Color.White),
                King(Position.from_description('E8'), Color.White),
                Bishop(Position.from_description('F8'), Color.White),
                Knight(Position.from_description('G8'), Color.White),
                Rook(Position.from_description('H8'), Color.White),
                Pawn(Position.from_description('A7'), Color.White),
                Pawn(Position.from_description('B7'), Color.White),
                Pawn(Position.from_description('C7'), Color.White),
                Pawn(Position.from_description('D7'), Color.White),
                Pawn(Position.from_description('E7'), Color.White),
                Pawn(Position.from_description('F7'), Color.White),
                Pawn(Position.from_description('G7'), Color.White),
                Pawn(Position.from_description('H7'), Color.White),

                Rook(Position.from_description('A1'), Color.Black),
                Knight(Position.from_description('B1'), Color.Black),
                Bishop(Position.from_description('C1'), Color.Black),
                Queen(Position.from_description('D1'), Color.Black),
                King(Position.from_description('E1'), Color.Black),
                Bishop(Position.from_description('F1'), Color.Black),
                Knight(Position.from_description('G1'), Color.Black),
                Rook(Position.from_description('H1'), Color.Black),
                Pawn(Position.from_description('A2'), Color.Black),
                Pawn(Position.from_description('B2'), Color.Black),
                Pawn(Position.from_description('C2'), Color.Black),
                Pawn(Position.from_description('D2'), Color.Black),
                Pawn(Position.from_description('E2'), Color.Black),
                Pawn(Position.from_description('F2'), Color.Black),
                Pawn(Position.from_description('G2'), Color.Black),
                Pawn(Position.from_description('H2'), Color.Black)
            ]
        else:
            self.board = [
                Rook(Position.from_description('A8'), Color.Black),
                Knight(Position.from_description('B8'), Color.Black),
                Bishop(Position.from_description('C8'), Color.Black),
                Queen(Position.from_description('D8'), Color.Black),
                King(Position.from_description('E8'), Color.Black),
                Bishop(Position.from_description('F8'), Color.Black),
                Knight(Position.from_description('G8'), Color.Black),
                Rook(Position.from_description('H8'), Color.Black),
                Pawn(Position.from_description('A7'), Color.Black),
                Pawn(Position.from_description('B7'), Color.Black),
                Pawn(Position.from_description('C7'), Color.Black),
                Pawn(Position.from_description('D7'), Color.Black),
                Pawn(Position.from_description('E7'), Color.Black),
                Pawn(Position.from_description('F7'), Color.Black),
                Pawn(Position.from_description('G7'), Color.Black),
                Pawn(Position.from_description('H7'), Color.Black),

                Rook(Position.from_description('A1'), Color.White),
                Knight(Position.from_description('B1'), Color.White),
                Bishop(Position.from_description('C1'), Color.White),
                Queen(Position.from_description('D1'), Color.White),
                King(Position.from_description('E1'), Color.White),
                Bishop(Position.from_description('F1'), Color.White),
                Knight(Position.from_description('G1'), Color.White),
                Rook(Position.from_description('H1'), Color.White),
                Pawn(Position.from_description('A2'), Color.White),
                Pawn(Position.from_description('B2'), Color.White),
                Pawn(Position.from_description('C2'), Color.White),
                Pawn(Position.from_description('D2'), Color.White),
                Pawn(Position.from_description('E2'), Color.White),
                Pawn(Position.from_description('F2'), Color.White),
                Pawn(Position.from_description('G2'), Color.White),
                Pawn(Position.from_description('H2'), Color.White)
            ]

    def print_board(self, moves: tuple[Move] = None):
        classes = [Pawn, Bishop, Knight, Rook, Queen, King]
        symbols = [['♟︎', '♝', '♞', '♜', '♛', '♚'],
                   ['♙', '♗', '♘', '♖', '♕', '♔']]
        print('┌───────────────────┐')
        print(f'│  {Back.BLACK + Fore.WHITE}A{Style.RESET_ALL} {Back.WHITE + Fore.BLACK}B{Style.RESET_ALL} {Back.BLACK + Fore.WHITE}C{Style.RESET_ALL} {Back.WHITE + Fore.BLACK}D{Style.RESET_ALL} {Back.BLACK + Fore.WHITE}E{Style.RESET_ALL} {Back.WHITE + Fore.BLACK}F{Style.RESET_ALL} {Back.BLACK + Fore.WHITE}G{Style.RESET_ALL} {Back.WHITE + Fore.BLACK}H{Style.RESET_ALL}  │')
        print('│ ┌───────────────┐ │')
        for y in range(8):
            row = []
            for x in range(8):
                piece = self.get(Position.from_coordinates((x + 1, y + 1)))
                is_move = False
                if moves:
                    for move in moves:
                        if Position.from_coordinates((x + 1,y + 1)).coordinates == move.b.coordinates:
                            is_move = True
                if piece is None:
                    row.append(f'{Back.WHITE + Fore.BLACK if (y % 2 == 0 and x % 2 == 0) or (y % 2 == 1 and x % 2 == 1) else Back.BLACK + Fore.WHITE}{" " if not is_move else "*"}{Style.RESET_ALL}')
                else:
                    for piece_class, symbol in zip(classes, symbols[int(piece.color.value / 2 + 1)]):
                        if type(piece) == piece_class:
                            if piece.focused:
                                row.append(Fore.LIGHTCYAN_EX + symbol + Style.RESET_ALL)
                            elif is_move:
                                row.append(Fore.RED + symbol + Style.RESET_ALL)
                            else:
                                row.append(symbol)

            print(f'│{Fore.WHITE + Back.BLACK if y % 2 == 0 else Fore.BLACK + Back.WHITE}{y + 1}{Style.RESET_ALL}│{" ".join(row)}│{Fore.WHITE + Back.BLACK if y % 2 == 1 else Fore.BLACK + Back.WHITE}{y + 1}{Style.RESET_ALL}│')
        print('│ └───────────────┘ │')
        print(f'│  {Back.WHITE + Fore.BLACK}A{Style.RESET_ALL} {Back.BLACK + Fore.WHITE}B{Style.RESET_ALL} {Back.WHITE + Fore.BLACK}C{Style.RESET_ALL} {Back.BLACK + Fore.WHITE}D{Style.RESET_ALL} {Back.WHITE + Fore.BLACK}E{Style.RESET_ALL} {Back.BLACK + Fore.WHITE}F{Style.RESET_ALL} {Back.WHITE + Fore.BLACK}G{Style.RESET_ALL} {Back.BLACK + Fore.WHITE}H{Style.RESET_ALL}  │')
        print('└───────────────────┘')

    def is_free(self, position: Position) -> bool:
        for piece in self.board:
            if piece.position.coordinates == position.coordinates:
                return False
        return position.is_legitimate()

    def get(self, position: Position) -> Piece or None:
        for piece in self.board:
            if piece.position.coordinates == position.coordinates:
                return piece
        return None

    def apply_move(self, move: Move):
        piece = self.get(move.a)
        if other_piece := self.get(move.b):
            self.board.remove(other_piece)
        piece.position = move.b


class Position:
    def __init__(self, x: int, y: int):
        self.coordinates = Vec2d(x, y)
        self.description = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'][x - 1] + str(y) if self.is_legitimate() else None

    @staticmethod
    def from_coordinates(coordinates: tuple[int, int]):
        return Position(coordinates[0], coordinates[1])

    @staticmethod
    def from_description(description: str):
        assert re.fullmatch('[A-H][1-8]', description)
        x = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'].index(description[0]) + 1
        y = int(description[1])
        return Position(x, y)

    def is_legitimate(self) -> bool:
        return self.coordinates.x in range(1, 9) and self.coordinates.y in range(1, 9)

    def __eq__(self, other):
        return other.description == self.description


class Color(Enum):
    White = -1
    Black = +1


class Move:
    def __init__(self, a: Position, b: Position):
        self.a = a
        self.b = b

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

    def __hash__(self):
        return int.from_bytes(sha256(f'{self.a}{self.b}'.encode()).digest(), 'big')


class Piece(ABC):
    def __init__(self, position: Position, color: Color):
        self.position = position
        self.color = color
        self.focused = False

    @abstractmethod
    def get_all_moves(self, engine: Engine) -> tuple[Move]:
        pass

    def get_possible_moves(self, engine: Engine) -> tuple[Move]:
        all_moves = self.get_all_moves(engine)
        return all_moves


class Pawn(Piece):
    def __init__(self, position: Position, color: Color):
        super().__init__(position, color)
        self.init_position = position

    def get_all_moves(self, engine) -> list[Move]:
        moves = []
        if engine.is_free(Position.from_coordinates(self.position.coordinates + self.color.value * Vec2d(0, 1))):
            moves.append(Move(self.position, Position.from_coordinates(self.position.coordinates + self.color.value * Vec2d(0, 1))))
        if self.init_position.description is self.position.description and Position.from_coordinates(self.position.coordinates + self.color.value * Vec2d(0, 2)).is_legitimate():
            moves.append(Move(self.position, Position.from_coordinates(self.position.coordinates + self.color.value * Vec2d(0, 2))))

        up_right = Position.from_coordinates(self.position.coordinates + Vec2d(1, self.color.value))
        up_left = Position.from_coordinates(self.position.coordinates + Vec2d(-1, self.color.value))

        if not engine.is_free(up_right) or (not up_right.is_legitimate()) or (engine.get(up_right) is not None and engine.get(up_right).color == self.color):
            moves.append(
                Move(self.position, up_right)
            )

        if not engine.is_free(up_left) or (not up_left.is_legitimate()) or (engine.get(up_left) is not None and engine.get(up_left).color == self.color):
            moves.append(
                Move(self.position, up_left)
            )

        return moves


class Bishop(Piece):
    def get_all_moves(self, engine) -> list[Move]:
        moves = []
        for i in range(1, 8):
            position = Position.from_coordinates(Vec2d(i, i) + self.position.coordinates)
            if (not position.is_legitimate()) or (engine.get(position) is not None and engine.get(position).color == self.color):
                break
            moves.append(Move(self.position, position))
            if not engine.is_free(position):
                break
        for i in range(1, 8):
            position = Position.from_coordinates(Vec2d(-i, i) + self.position.coordinates)
            if (not position.is_legitimate()) or (engine.get(position) is not None and engine.get(position).color == self.color):
                break
            moves.append(Move(self.position, position))
            if not engine.is_free(position):
                break

        for i in range(1, 8):
            position = Position.from_coordinates(Vec2d(i, -i) + self.position.coordinates)
            if (not position.is_legitimate()) or (engine.get(position) is not None and engine.get(position).color == self.color):
                break
            moves.append(Move(self.position, position))
            if not engine.is_free(position):
                break

        for i in range(1, 8):
            position = Position.from_coordinates(Vec2d(-i, -i) + self.position.coordinates)
            if (not position.is_legitimate()) or (engine.get(position) is not None and engine.get(position).color == self.color):
                break
            moves.append(Move(self.position, position))
            if not engine.is_free(position):
                break

        return moves


class Knight(Piece):
    def get_all_moves(self, engine) -> list[Move]:
        offsets = [
            Vec2d(2,1),
            Vec2d(2,-1),
            Vec2d(-2,1),
            Vec2d(-2,-1),
            Vec2d(1,2),
            Vec2d(-1,2),
            Vec2d(1,-2),
            Vec2d(-1,-2)
        ]

        moves = []
        for offset in offsets:
            position = Position.from_coordinates(offset + self.position.coordinates)
            if (position.is_legitimate()) and (engine.get(position) is None or engine.get(position).color != self.color):
                moves.append(Move(self.position, position))

        return moves


class Rook(Piece):
    def get_all_moves(self, engine) -> list[Move]:
        moves = []
        for i in range(1, 8):
            position = Position.from_coordinates(Vec2d(i, 0) + self.position.coordinates)
            if (not position.is_legitimate()) or (engine.get(position) is not None and engine.get(position).color == self.color):
                break
            moves.append(Move(self.position, position))
            if not engine.is_free(position):
                break

        for i in range(1, 8):
            position = Position.from_coordinates(Vec2d(-i, 0) + self.position.coordinates)
            if (not position.is_legitimate()) or (engine.get(position) is not None and engine.get(position).color == self.color):
                break
            moves.append(Move(self.position, position))
            if not engine.is_free(position):
                break

        for i in range(1, 8):
            position = Position.from_coordinates(Vec2d(0, i) + self.position.coordinates)
            if (not position.is_legitimate()) or (engine.get(position) is not None and engine.get(position).color == self.color):
                break
            moves.append(Move(self.position, position))
            if not engine.is_free(position):
                break

        for i in range(1, 8):
            position = Position.from_coordinates(Vec2d(0, -i) + self.position.coordinates)
            if (not position.is_legitimate()) or (engine.get(position) is not None and engine.get(position).color == self.color):
                break
            moves.append(Move(self.position, position))
            if not engine.is_free(position):
                break

        return moves


class Queen(Piece):
    def get_all_moves(self, engine) -> list[Move]:
        moves = []
        if (position := Position.from_coordinates(self.position.coordinates - Vec2d(0, self.color.value))).is_legitimate() and (engine.get(position) == None or engine.get(position).color != self.color):
            moves.append(Move(self.position, position))

        for i in range(1, 8):
            position = Position.from_coordinates(Vec2d(i, 0) + self.position.coordinates)
            if (not position.is_legitimate()) or (engine.get(position) is not None and engine.get(position).color == self.color):
                break
            moves.append(Move(self.position, position))
            if not engine.is_free(position):
                break

        for i in range(1, 8):
            position = Position.from_coordinates(Vec2d(-i, 0) + self.position.coordinates)
            if (not position.is_legitimate()) or (engine.get(position) is not None and engine.get(position).color == self.color):
                break
            moves.append(Move(self.position, position))
            if not engine.is_free(position):
                break

        for i in range(1, 8):
            position = Position.from_coordinates(Vec2d(0, i * self.color.value) + self.position.coordinates)
            if (not position.is_legitimate()) or (engine.get(position) is not None and engine.get(position).color == self.color):
                break
            moves.append(Move(self.position, position))
            if not engine.is_free(position):
                break

        for i in range(1, 8):
            position = Position.from_coordinates(Vec2d(i, i) + self.position.coordinates)
            if (not position.is_legitimate()) or (engine.get(position) is not None and engine.get(position).color == self.color):
                break
            moves.append(Move(self.position, position))
            if not engine.is_free(position):
                break
        for i in range(1, 8):
            position = Position.from_coordinates(Vec2d(-i, i) + self.position.coordinates)
            if (not position.is_legitimate()) or (engine.get(position) is not None and engine.get(position).color == self.color):
                break
            moves.append(Move(self.position, position))
            if not engine.is_free(position):
                break

        for i in range(1, 8):
            position = Position.from_coordinates(Vec2d(i, -i) + self.position.coordinates)
            if (not position.is_legitimate()) or (engine.get(position) is not None and engine.get(position).color == self.color):
                break
            moves.append(Move(self.position, position))
            if not engine.is_free(position):
                break

        for i in range(1, 8):
            position = Position.from_coordinates(Vec2d(-i, -i) + self.position.coordinates)
            if (not position.is_legitimate()) or (engine.get(position) is not None and engine.get(position).color == self.color):
                break
            moves.append(Move(self.position, position))
            if not engine.is_free(position):
                break

        return moves


class King(Piece):
    def get_all_moves(self, engine) -> list[Move]:
        moves = []
        for x in [-1,0,1]:
            for y in [-1,0,1]:
                position = Position.from_coordinates(Vec2d(x, y) + self.position.coordinates)
                if position.is_legitimate() and (engine.get(position) is None or engine.get(position).color != self.color):
                    moves.append(Move(self.position, position))
        return moves