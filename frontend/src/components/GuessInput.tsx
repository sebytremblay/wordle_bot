import React, { useState } from 'react';
import styled from 'styled-components';
import { GuessInputProps } from '../types/components';

const Input = styled.input`
    padding: 10px;
    font-size: 1.2rem;
    width: 200px;
    text-transform: uppercase;
    text-align: center;
    border: 2px solid #ccc;
    border-radius: 4px;
    margin: 10px 0;

    &:disabled {
        background-color: #f0f0f0;
        cursor: not-allowed;
    }
`;

const GuessInput: React.FC<GuessInputProps> = ({ onSubmit, disabled }) => {
    const [guess, setGuess] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (guess.length === 5) {
            onSubmit(guess.toUpperCase());
            setGuess('');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <Input
                type="text"
                value={guess}
                onChange={(e) => setGuess(e.target.value.slice(0, 5))}
                disabled={disabled}
                maxLength={5}
                placeholder="Enter guess"
            />
        </form>
    );
};

export default GuessInput; 