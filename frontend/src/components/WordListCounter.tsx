import React from 'react';
import styled from '@emotion/styled';

interface WordListCounterProps {
    count: number;
}

const Counter = styled.div`
  max-width: 350px;
  margin: 10px auto;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
  text-align: center;
  font-size: 1.1rem;
  color: #538d4e;
`;

const WordListCounter: React.FC<WordListCounterProps> = ({ count }) => (
    <Counter>
        {count === 1 ? (
            'Only 1 word remaining!'
        ) : (
            `${count} possible words remaining`
        )}
    </Counter>
);

export default WordListCounter; 