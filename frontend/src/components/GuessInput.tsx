import React, { useState, FormEvent } from 'react';
import { GameState } from '../types/game';
import { submitGuess } from '../services/api';
import { Form, Input, Button, ErrorMessage } from '../styles/components/GuessInput.styles';

interface GuessInputProps {
    gameId: string;
    onGuessUpdate: (state: GameState) => void;
    disabled?: boolean;
}

const GuessInput: React.FC<GuessInputProps> = ({ gameId, onGuessUpdate, disabled }) => {
    const [guess, setGuess] = useState('');
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        if (guess.length !== 5) {
            setError('Guess must be 5 letters');
            return;
        }

        try {
            const response = await submitGuess(gameId, guess.toLowerCase());
            onGuessUpdate({
                state: response.state,
                game_id: gameId,
                message: response.message,
                error: response.error
            });
            setGuess('');
            setError(null);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred');
        }
    };

    return (
        <Form onSubmit={handleSubmit}>
            <Input
                type="text"
                value={guess}
                onChange={(e) => {
                    const value = e.target.value.toUpperCase();
                    if (value.length <= 5 && /^[A-Z]*$/.test(value)) {
                        setGuess(value);
                        setError(null);
                    }
                }}
                placeholder="Enter guess"
                maxLength={5}
                disabled={disabled}
                aria-label="Enter your guess"
            />
            <Button type="submit" disabled={disabled || guess.length !== 5}>
                Submit
            </Button>
            {error && <ErrorMessage role="alert">{error}</ErrorMessage>}
        </Form>
    );
};

export default GuessInput; 