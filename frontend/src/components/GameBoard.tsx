import React from 'react';
import { GameState, GuessEntry } from '../types/game';
import { FeedbackType } from '../types/common';
import styled from '@emotion/styled';

interface GameBoardProps {
    state: GameState;
}

interface CellProps {
    status?: 'correct' | 'present' | 'absent';
}

interface ProcessedCell {
    letter: string;
    status: 'correct' | 'present' | 'absent';
}

const Grid = styled.div`
  display: grid;
  grid-template-rows: repeat(6, 1fr);
  gap: 5px;
  padding: 10px;
  width: 350px;
  margin: 0 auto;
  
  @media (min-width: 500px) {
    width: 390px;
  }
`;

const Row = styled.div`
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 5px;
`;

const Cell = styled.div<CellProps>`
  width: 100%;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  aspect-ratio: 1;
  font-size: 2rem;
  font-weight: bold;
  vertical-align: middle;
  box-sizing: border-box;
  color: ${(props: CellProps) => props.status ? 'white' : 'black'};
  text-transform: uppercase;
  user-select: none;
  
  border: 2px solid ${(props: CellProps) => props.status ? 'transparent' : '#d3d6da'};
  background-color: ${(props: CellProps) => {
        switch (props.status) {
            case 'correct':
                return '#6aaa64';
            case 'present':
                return '#c9b458';
            case 'absent':
                return '#787c7e';
            default:
                return 'white';
        }
    }};
  
  transform-style: preserve-3d;
  transition: transform 0.6s;
  transform: ${(props: CellProps) => props.status ? 'rotateX(360deg)' : 'none'};
  
  @media (min-width: 500px) {
    font-size: 2.25rem;
  }
`;

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

const GameBoard: React.FC<GameBoardProps> = ({ state }) => {
    console.log('GameBoard rendering with state:', state);
    console.log('History:', state.state.history);

    // Create a 6x5 grid of empty cells
    const emptyGrid = Array(6).fill(null).map(() => Array(5).fill(''));

    // Fill in the grid with guesses and their feedback
    const grid = emptyGrid.map((row, rowIndex) => {
        const guessEntry = state.state.history[rowIndex];
        console.log(`Processing row ${rowIndex}, guess:`, guessEntry);

        if (!guessEntry || !Array.isArray(guessEntry) || guessEntry.length !== 2) {
            console.log(`No valid guess for row ${rowIndex}`);
            return row;
        }

        const [word, feedback] = guessEntry;
        if (!word || !feedback || !Array.isArray(feedback)) {
            console.warn(`Row ${rowIndex} has invalid guess structure:`, guessEntry);
            return row;
        }

        // Split the guess string into an array of characters
        const letters = word.split('');
        console.log(`Row ${rowIndex} letters:`, letters);
        console.log(`Row ${rowIndex} feedback:`, feedback);

        const processedRow = letters.map((letter: string, colIndex: number) => {
            const status = getFeedbackStatus(feedback[colIndex] as FeedbackType);
            console.log(`Cell ${rowIndex},${colIndex}: letter=${letter}, status=${status}`);
            return {
                letter,
                status
            };
        });

        console.log(`Processed row ${rowIndex}:`, processedRow);
        return processedRow;
    });

    console.log('Final grid structure:', grid);

    return (
        <Grid>
            {grid.map((row, rowIndex) => {
                console.log(`Rendering row ${rowIndex}:`, row);
                return (
                    <Row key={rowIndex}>
                        {row.map((cell: string | ProcessedCell, colIndex: number) => {
                            console.log(`Rendering cell ${rowIndex},${colIndex}:`, cell);
                            return (
                                <Cell
                                    key={`${rowIndex}-${colIndex}`}
                                    status={typeof cell === 'string' ? undefined : cell.status}
                                >
                                    {typeof cell === 'string' ? '' : cell.letter}
                                </Cell>
                            );
                        })}
                    </Row>
                );
            })}
        </Grid>
    );
};

export default GameBoard; 