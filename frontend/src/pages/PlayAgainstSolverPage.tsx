import React, { useEffect, useState } from 'react';
import styled from '@emotion/styled';
import Header from '../components/Header';
import Footer from '../components/Footer';
import GameBoard from '../components/GameBoard';
import GuessInput from '../components/GuessInput';
import SolverSelect from '../components/PlayAgainstSolverPage/SolverSelect';
import WordListCounter from '../components/WordListCounter';
import { startNewGame, getSolvers, startMirrorGame, getHint, submitGuess } from '../services/api';
import { GameState } from '../types/game';

const Container = styled.div`
    max-width: 800px;
    margin: 0 auto;
    padding: 0 1rem;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
`;

const GameContainer = styled.div`
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
    justify-content: center;
    margin-bottom: 2rem;
`;

const GameSection = styled.div`
    text-align: center;
`;

const GameTitle = styled.h2`
    color: #1a1a1b;
    margin-bottom: 1rem;
`;

const Content = styled.main`
    flex: 1;
    display: flex;
    flex-direction: column;
`;

const SolverSelectContainer = styled.div`
    display: flex;
    justify-content: center;
    width: 100%;
    margin: 1rem 0;
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

const PlayAgainstSolverPage: React.FC = () => {
    const [playerGameState, setPlayerGameState] = useState<GameState | null>(null);
    const [solverGameState, setSolverGameState] = useState<GameState | null>(null);
    const [selectedSolver, setSelectedSolver] = useState<string>('');
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const initGame = async () => {
            try {
                const solversResponse = await getSolvers();
                setSelectedSolver(solversResponse.solvers[0]?.id || '');

                const playerGame = await startNewGame();
                setPlayerGameState(playerGame);

                const solverGame = await startMirrorGame(playerGame.game_id, selectedSolver);
                setSolverGameState(solverGame);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Failed to start game');
            }
        };

        initGame();
    }, []);

    const handleNewGame = async () => {
        try {
            setIsLoading(true);
            const playerGame = await startNewGame();
            setPlayerGameState(playerGame);

            const solverGame = await startMirrorGame(playerGame.game_id, selectedSolver);
            setSolverGameState(solverGame);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to start new game');
        } finally {
            setIsLoading(false);
        }
    };

    if (error) {
        return (
            <Container>
                <Header />
                <ErrorMessage>{error}</ErrorMessage>
                <Footer />
                <NewGameButton onClick={async () => {
                    try {
                        await handleNewGame();
                    } catch (err) {
                        setError(err instanceof Error ? err.message : 'Failed to start new game');
                    }
                }}>
                    New Game
                </NewGameButton>
            </Container>
        );
    }

    if (!playerGameState || !solverGameState) {
        return (
            <Container>
                <Header />
                <LoadingMessage>Starting new game...</LoadingMessage>
                <Footer />
            </Container>
        );
    }

    const onGuessUpdate = (gameState: GameState) => {
        // Update the player game state
        setPlayerGameState(gameState);

        // Make a guess with the solver and update its state
        makeSolverGuess();
    };

    const makeSolverGuess = async () => {
        setIsLoading(true);

        try {
            const hint = await getHint(solverGameState.game_id, selectedSolver);
            const solverGame = await submitGuess(solverGameState.game_id, hint.hint);
            setSolverGameState({
                state: solverGame.state,
                game_id: solverGame.game_id,
            });
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to make solver guess');
        } finally {
            setIsLoading(false);
        }
    };

    const isGameOver = playerGameState.state.game_over || solverGameState.state.game_over;

    return (
        <Container>
            <Header />
            <Content>
                <SolverSelectContainer>
                    <SolverSelect
                        onChange={(e) => setSelectedSolver(e.target.value)}
                        disabled={isGameOver || isLoading}
                    />
                </SolverSelectContainer>
                <GameContainer>
                    <GameSection>
                        <GameTitle>Your Game</GameTitle>
                        <GameBoard state={playerGameState} />
                    </GameSection>
                    <GameSection>
                        <GameTitle>Solver's Game</GameTitle>
                        <GameBoard state={solverGameState} hideLetters={true} />
                    </GameSection>
                </GameContainer>
                <GuessInput
                    gameId={playerGameState.game_id}
                    onGuessUpdate={onGuessUpdate}
                    disabled={isGameOver || isLoading}
                />
                {!isGameOver && (
                    <WordListCounter
                        count={playerGameState.state.candidates_remaining}
                        gameId={playerGameState.game_id}
                    />
                )}
                {isGameOver && (
                    <>
                        <GameOverMessage $won={playerGameState.state.game_won}>
                            {playerGameState.state.game_won ? 'Congratulations!' : 'Game Over!'}
                        </GameOverMessage>
                        <NewGameButton onClick={async () => {
                            try {
                                await handleNewGame();
                            } catch (err) {
                                setError(err instanceof Error ? err.message : 'Failed to start new game');
                            }
                        }}>
                            New Game
                        </NewGameButton>
                    </>
                )}
            </Content>
            <Footer />
        </Container>
    );
};

export default PlayAgainstSolverPage; 