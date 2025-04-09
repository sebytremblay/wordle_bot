import React from 'react';
import { GameState } from '../types/game';
import { FeedbackType } from '../types/common';
import { Grid, Row, Cell } from '../styles/components/GameBoard.styles';

interface GameBoardProps {
    state: GameState;
    hideLetters?: boolean;
}

interface ProcessedCell {
    letter: string;
    status: 'correct' | 'present' | 'absent';
}

const getFeedbackStatus = (feedback: FeedbackType): 'correct' | 'present' | 'absent' => {
    switch (feedback) {
        case 2:
            return 'correct';
        case 1:
            return 'present';
        case 0:
        default:
            return 'absent';
    }
};

const GameBoard: React.FC<GameBoardProps> = ({ state, hideLetters = false }) => {
    // Create a 6x5 grid of empty cells
    const emptyGrid = Array(6).fill(null).map(() => Array(5).fill(''));

    // Fill in the grid with guesses and their feedback
    const grid = emptyGrid.map((row, rowIndex) => {
        const guessEntry = state.state.history[rowIndex];

        if (!guessEntry || !Array.isArray(guessEntry) || guessEntry.length !== 2) {
            return row;
        }

        const [word, feedback] = guessEntry;
        if (!word || !feedback || !Array.isArray(feedback)) {
            return row;
        }

        // Split the guess string into an array of characters
        const letters = word.split('');

        const processedRow = letters.map((letter: string, colIndex: number) => {
            const status = getFeedbackStatus(feedback[colIndex] as FeedbackType);
            return {
                letter,
                status
            };
        });

        return processedRow;
    });

    return (
        <Grid>
            {grid.map((row, rowIndex) => (
                <Row key={rowIndex}>
                    {row.map((cell: string | ProcessedCell, colIndex: number) => (
                        <Cell
                            key={`${rowIndex}-${colIndex}`}
                            status={typeof cell === 'string' ? undefined : cell.status}
                        >
                            {typeof cell === 'string' || hideLetters ? '' : cell.letter}
                        </Cell>
                    ))}
                </Row>
            ))}
        </Grid>
    );
};

export default GameBoard; 