import React, { useState } from 'react';
import styled from '@emotion/styled';
import WordListPopup from './WordListPopup';

interface WordListCounterProps {
    count: number;
    gameId: string;
}

const Counter = styled.button`
    width: 100%;
    max-width: 350px;
    margin: 10px auto;
    padding: 12px 15px;
    background-color: #f8f9fa;
    border: 2px solid #e9ecef;
    border-radius: 8px;
    text-align: center;
    font-size: 1.1rem;
    color: #538d4e;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    position: relative;
    font-family: inherit;

    &:hover {
        background-color: #e9ecef;
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    &:active {
        transform: translateY(0);
    }

    &::after {
        position: absolute;
        bottom: -20px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 0.8rem;
        color: #787c7e;
        opacity: 0;
        transition: opacity 0.2s ease;
    }

    &:hover::after {
        opacity: 1;
    }
`;

const WordListCounter: React.FC<WordListCounterProps> = ({ count, gameId }) => {
    const [isPopupOpen, setIsPopupOpen] = useState(false);
    const [words, setWords] = useState<string[]>([]);
    const [isLoading, setIsLoading] = useState(false);

    const handleClick = async () => {
        if (!isLoading) {
            setIsLoading(true);
            try {
                const response = await fetch(`${process.env.REACT_APP_API_URL}/remaining-words?game_id=${gameId}`);
                const data = await response.json();
                if (response.ok) {
                    setWords(data.words);
                    setIsPopupOpen(true);
                } else {
                    console.error('Failed to fetch remaining words:', data.error);
                }
            } catch (error) {
                console.error('Error fetching remaining words:', error);
            } finally {
                setIsLoading(false);
            }
        }
    };

    return (
        <>
            <Counter onClick={handleClick} type="button">
                {isLoading ? (
                    'Loading...'
                ) : (
                    <>
                        <span>
                            {count === 1 ? 'Only 1 word remaining!' : `${count} possible words remaining`}
                        </span>
                        <span role="img" aria-label="click to view">🔍</span>
                    </>
                )}
            </Counter>
            <WordListPopup
                isOpen={isPopupOpen}
                onClose={() => setIsPopupOpen(false)}
                words={words}
            />
        </>
    );
};

export default WordListCounter; 