import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { GameState } from '../types/game';
import { startNewGame, submitGuess } from '../services/api';
import GameBoard from './GameBoard';
import GuessInput from './GuessInput';
import HintPanel from './HintPanel';
import { logger } from '../utils/logger';

const Container = styled.div`
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
`;

const GameContainer = styled.div`
    display: flex;
    gap: 20px;
    margin-top: 20px;

    @media (max-width: 768px) {
        flex-direction: column;
    }
`;

const MainColumn = styled.div`
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
`;

const SideColumn = styled.div`
    width: 300px;

    @media (max-width: 768px) {
        width: 100%;
    }
`;

const GameStatus = styled.div`
    text-align: center;
    margin: 20px 0;
    font-size: 1.2rem;
    font-weight: bold;
    color: ${props => props.theme.colors?.primary || '#6aaa64'};
`;

const Button = styled.button`
    padding: 10px 20px;
    font-size: 1rem;
    background-color: #6aaa64;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;

    &:hover {
        background-color: #538d4e;
    }
`;

const HomePage: React.FC = () => {
    const [gameState, setGameState] = useState<GameState>();
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        initializeGame();
    }, []);

    const initializeGame = async () => {
        try {
            logger.debug('HomePage', 'Initializing new game');
            const newState = await startNewGame();
            setGameState(newState);
            setError(null);
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Failed to start game';
            logger.error('HomePage', 'Failed to initialize game:', err);
            setError(errorMessage);
        }
    };

    const handleGuess = async (guess: string) => {
        if (!gameState) {
            setError('Game not initialized');
            return;
        }

        try {
            logger.debug('HomePage', 'Submitting guess:', guess);
            const response = await submitGuess(gameState.game_id, guess);
            // Transform GuessResponse to GameState
            const newState: GameState = {
                game_id: gameState.game_id,
                state: response.state,
                message: response.message,
                error: response.error
            };
            setGameState(newState);
            setError(null);
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Failed to submit guess';
            logger.error('HomePage', 'Failed to submit guess:', err);
            setError(errorMessage);
        }
    };

    if (error) {
        return (
            <Container>
                <div>Error: {error}</div>
                <Button onClick={initializeGame}>Try Again</Button>
            </Container>
        );
    }

    if (!gameState) {
        return <Container>Loading...</Container>;
    }

    const isGameOver = gameState.state.game_over;
    const hasWon = gameState.state.game_won;

    return (
        <Container>
            <GameContainer>
                <MainColumn>
                    <GameBoard state={gameState} />
                    <GuessInput
                        onSubmit={handleGuess}
                        disabled={isGameOver}
                    />
                    {isGameOver && (
                        <GameStatus>
                            <p>{hasWon ? 'Congratulations!' : 'Game Over!'}</p>
                            <Button onClick={initializeGame}>Play Again</Button>
                        </GameStatus>
                    )}
                </MainColumn>
                <SideColumn>
                    <HintPanel
                        gameId={gameState.game_id}
                        disabled={isGameOver}
                    />
                </SideColumn>
            </GameContainer>
        </Container>
    );
};

export default HomePage; 