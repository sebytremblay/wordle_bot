import React, { useEffect, useState } from 'react';
import styled from '@emotion/styled';
import GameBoard from '../components/GameBoard';
import GuessInput from '../components/GuessInput';
import { startNewGame, startMirrorGame, getHint, getSolvers, submitGuess } from '../services/api';
import { GameState } from '../types/game';
import { SolverInfo } from '../types/solvers';

const Container = styled.div`
    max-width: 1200px;
    margin: 60px auto 0;
    padding: 2rem 1rem;
`;

const Title = styled.h1`
    text-align: center;
    color: #1a1a1b;
    margin-bottom: 2rem;
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

const LoadingSpinner = styled.div`
    border: 4px solid #f3f3f3;
    border-top: 4px solid #6aaa64;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 2rem auto;

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
`;

const SolverSelect = styled.select`
    padding: 0.5rem;
    margin: 1rem;
    font-size: 1rem;
    border: 2px solid #d3d6da;
    border-radius: 4px;
    background-color: white;
    cursor: pointer;

    &:focus {
        outline: none;
        border-color: #6aaa64;
    }
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
    const [solvers, setSolvers] = useState<SolverInfo[]>([]);
    const [selectedSolver, setSelectedSolver] = useState<string>('');
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const initGame = async () => {
            try {
                const solversResponse = await getSolvers();
                setSolvers(solversResponse.solvers);
                setSelectedSolver(solversResponse.solvers[0]?.id || '');

                const playerGame = await startNewGame();
                setPlayerGameState(playerGame.state);

                const solverGame = await startMirrorGame(playerGame.game_id, solversResponse.solvers[0]?.id);
                setSolverGameState(solverGame.state);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Failed to initialize games');
            }
        };

        initGame();
    }, []);

    const handleGuessSubmit = async (gameId: string, guess: string) => {
        if (!playerGameState || !solverGameState) return;

        setIsLoading(true);
        try {
            // Submit player's guess
            const playerResponse = await submitGuess(gameId, guess);
            setPlayerGameState(playerResponse.state);

            if (!playerResponse.state.state.game_over) {
                // Get solver's guess
                const solverHint = await getHint(solverGameState.game_id, selectedSolver);
                const solverResponse = await submitGuess(solverGameState.game_id, solverHint.hint);
                setSolverGameState(solverResponse.state);
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to process guess');
        } finally {
            setIsLoading(false);
        }
    };

    const handleNewGame = async () => {
        try {
            setIsLoading(true);
            const playerGame = await startNewGame();
            setPlayerGameState(playerGame.state);

            const solverGame = await startMirrorGame(playerGame.game_id, selectedSolver);
            setSolverGameState(solverGame.state);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to start new game');
        } finally {
            setIsLoading(false);
        }
    };

    if (error) {
        return (
            <Container>
                <Title>Error</Title>
                <p style={{ textAlign: 'center', color: 'red' }}>{error}</p>
                <NewGameButton onClick={handleNewGame}>Try Again</NewGameButton>
            </Container>
        );
    }

    if (!playerGameState || !solverGameState) {
        return (
            <Container>
                <Title>Loading</Title>
                <LoadingSpinner />
            </Container>
        );
    }

    const isGameOver = playerGameState.state.game_over || solverGameState.state.game_over;

    return (
        <Container>
            <Title>Play Against a Solver</Title>
            <SolverSelect
                value={selectedSolver}
                onChange={(e) => setSelectedSolver(e.target.value)}
                disabled={isLoading}
            >
                {solvers.map((solver) => (
                    <option key={solver.id} value={solver.id}>
                        {solver.name}
                    </option>
                ))}
            </SolverSelect>
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
            {isLoading && <LoadingSpinner />}
            <GuessInput
                gameId={playerGameState.game_id}
                onGuessUpdate={setPlayerGameState}
                disabled={isLoading || isGameOver}
            />
            {isGameOver && (
                <NewGameButton onClick={handleNewGame}>
                    New Game
                </NewGameButton>
            )}
        </Container>
    );
};

export default PlayAgainstSolverPage; 