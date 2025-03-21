import React from 'react';
import styled from 'styled-components';
import { GameBoardProps } from '../types/components';

const Board = styled.div`
    display: grid;
    grid-template-rows: repeat(6, 1fr);
    gap: 5px;
    margin: 20px 0;
`;

const Row = styled.div`
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 5px;
`;

const Cell = styled.div<{ feedback?: number }>`
    width: 60px;
    height: 60px;
    border: 2px solid #ccc;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    font-weight: bold;
    text-transform: uppercase;
    background-color: ${props => {
        switch (props.feedback) {
            case 2: return '#6aaa64'; // Correct
            case 1: return '#c9b458'; // Wrong position
            case 0: return '#787c7e'; // Not in word
            default: return '#ffffff';
        }
    }};
    color: white;
`;

const GameBoard: React.FC<GameBoardProps> = ({ state }) => {
    return (
        <Board>
            {Array.from({ length: 6 }).map((_, rowIndex) => (
                <Row key={rowIndex}>
                    {Array.from({ length: 5 }).map((_, colIndex) => {
                        const entry = state.state.history[rowIndex];
                        const letter = entry?.guess[colIndex];
                        const feedback = entry?.feedback[colIndex];
                        return (
                            <Cell key={colIndex} feedback={feedback}>
                                {letter}
                            </Cell>
                        );
                    })}
                </Row>
            ))}
        </Board>
    );
};

export default GameBoard; 