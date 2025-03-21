import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import Header from '../components/Header';
import GameBoard from '../components/GameBoard';
import GuessInput from '../components/GuessInput';
import HintPanel from '../components/HintPanel';
import { startNewGame, submitGuess } from '../services/api';
import { GameState } from '../types/game';
import { logger } from '../utils/logger';

const Container = styled.div`
    max-width: 500px;
    margin: 0 auto;
    padding: 0 20px;
`;

const NewGameButton = styled.button`
    display: block;
    margin: 20px auto;
    padding: 10px 20px;
    font-size: 1.2rem;
    background-color: ${props => props.theme.colors.primaryDark};
    color: ${props => props.theme.colors.white};
    border: none;
    border-radius: 4px;
    cursor: pointer;
    &:hover {
        background-color: ${props => props.theme.colors.primary};
    }
`;

const GameOverMessage = styled.div<{ $won: boolean }>`
    text-align: center;
    margin: 20px 0;
    font-size: 1.2rem;
    font-weight: bold;
    color: ${props => props.$won ? props.theme.colors.primary : props.theme.colors.gray};
`;

const LoadingMessage = styled.div`
    text-align: center;
    margin: 20px 0;
    font-size: 1.2rem;
    color: ${props => props.theme.colors.text};
`;

const ErrorMessage = styled.div`
    text-align: center;
    margin: 20px 0;
    font-size: 1.2rem;
    color: ${props => props.theme.colors.error};
`;

const HomePage: React.FC = () => {
    const [gameState, setGameState] = useState<GameState | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const initializeGame = async () => {
        setLoading(true);
        setError('');
        try {
            const response = await startNewGame();
            logger.debug('HomePage', 'New game started:', response);
            setGameState(response);
        } catch (err) {
            const error = err instanceof Error ? err.message : 'Failed to start game';
            setError(error);
            logger.error('HomePage', 'Error starting game:', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        initializeGame();
    }, []);

    if (loading) {
        return (
            <Container>
                <Header />
                <LoadingMessage>Loading...</LoadingMessage>
            </Container>
        );
    }

    if (error) {
        return (
            <Container>
                <Header />
                <ErrorMessage>{error}</ErrorMessage>
                <NewGameButton onClick={initializeGame}>Try Again</NewGameButton>
            </Container>
        );
    }

    if (!gameState) {
        return null;
    }

    return (
        <Container>
            <Header />
            <GameBoard state={gameState} />
            <GuessInput
                onSubmit={async (guess: string) => {
                    const response = await submitGuess(gameState.game_id, guess);
                    setGameState(response);
                }}
                disabled={gameState.state.game_over}
            />
            <HintPanel
                gameId={gameState.game_id}
                disabled={gameState.state.game_over}
            />
            {gameState.state.game_over && (
                <>
                    <GameOverMessage $won={gameState.state.game_won}>
                        {gameState.state.game_won ? 'Congratulations!' : 'Game Over!'}
                    </GameOverMessage>
                    <NewGameButton onClick={initializeGame}>
                        New Game
                    </NewGameButton>
                </>
            )}
        </Container>
    );
};

export default HomePage; 