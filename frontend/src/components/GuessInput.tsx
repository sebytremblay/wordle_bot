import React, { useState, FormEvent } from 'react';
import styled from '@emotion/styled';
import { GameState } from '../types/game';
import { submitGuess } from '../services/api';

interface GuessInputProps {
    gameId: string;
    onGuessUpdate: (state: GameState) => void;
    disabled?: boolean;
}

const Form = styled.form`
  display: flex;
  gap: 10px;
  max-width: 350px;
  margin: 20px auto;
`;

const Input = styled.input`
  flex: 1;
  padding: 10px;
  font-size: 1.2rem;
  border: 2px solid #d3d6da;
  border-radius: 4px;
  text-transform: uppercase;
  &:disabled {
    background-color: #f0f0f0;
    cursor: not-allowed;
  }
`;

const Button = styled.button`
  padding: 10px 20px;
  font-size: 1.2rem;
  background-color: #6aaa64;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  &:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
  &:hover:not(:disabled) {
    background-color: #538d4e;
  }
`;

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
            onGuessUpdate(response);
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
            {error && <div role="alert" style={{ color: 'red' }}>{error}</div>}
        </Form>
    );
};

export default GuessInput; 