import React, { useEffect, useState } from 'react';
import styled from '@emotion/styled';
import Header from '../components/Header';
import Footer from '../components/Footer';
import GameBoard from '../components/GameBoard';
import GuessInput from '../components/GuessInput';
import HintPanel from '../components/HintPanel';
import WordListCounter from '../components/WordListCounter';
import { startNewGame } from '../services/api';
import { GameState } from '../types/game';

const Container = styled.div`
    max-width: 800px;
    margin: 0 auto;
    padding: 0 1rem;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
`;

const Content = styled.main`
    flex: 1;
    display: flex;
    flex-direction: column;
`;

const LoadingMessage = styled.div`
    text-align: center;
    padding: 2rem;
    color: #787c7e;
    font-size: 1.2rem;
`;

const ErrorMessage = styled.div`
    text-align: center;
    padding: 2rem;
    color: red;
    font-size: 1.2rem;
`;

const GameOverMessage = styled.div<{ $won: boolean }>`
    text-align: center;
    padding: 2rem;
    font-size: 1.5rem;
    font-weight: bold;
    color: ${props => props.$won ? '#6aaa64' : '#dc3545'};
`;

const NewGameButton = styled.button`
    display: block;
    margin: 1rem auto;
    padding: 0.75rem 1.5rem;
    font-size: 1.1rem;
    background-color: #538d4e;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    &:hover {
        background-color: #3a6b37;
    }
`;

const HomePage: React.FC = () => {
    const [gameState, setGameState] = useState<GameState | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const initGame = async () => {
            try {
                const response = await startNewGame();
                setGameState(response);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Failed to start game');
            }
        };

        initGame();
    }, []);

    if (error) {
        return (
            <Container>
                <Header />
                <ErrorMessage>{error}</ErrorMessage>
                <Footer />
            </Container>
        );
    }

    if (!gameState) {
        return (
            <Container>
                <Header />
                <LoadingMessage>Starting new game...</LoadingMessage>
                <Footer />
            </Container>
        );
    }

    const isGameOver = gameState.state.game_over;

    return (
        <Container>
            <Header />
            <Content>
                <GameBoard state={gameState} />
                <GuessInput
                    gameId={gameState.game_id}
                    onGuessUpdate={setGameState}
                    disabled={isGameOver}
                />
                <HintPanel
                    gameId={gameState.game_id}
                    onHintReceived={setGameState}
                    disabled={isGameOver}
                />
                <WordListCounter count={gameState.state.candidates_remaining} />
            </Content>
            {isGameOver && (
                <>
                    <GameOverMessage $won={gameState.state.game_won}>
                        {gameState.state.game_won ? 'Congratulations!' : 'Game Over!'}
                    </GameOverMessage>
                    <NewGameButton onClick={async () => {
                        try {
                            const response = await startNewGame();
                            setGameState(response);
                        } catch (err) {
                            setError(err instanceof Error ? err.message : 'Failed to start new game');
                        }
                    }}>
                        New Game
                    </NewGameButton>
                </>
            )}
            <Footer />
        </Container>
    );
};

export default HomePage; 