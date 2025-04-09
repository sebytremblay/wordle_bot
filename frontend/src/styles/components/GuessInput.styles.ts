import styled from '@emotion/styled';
import { theme } from '../theme';

export const Form = styled.form`
    display: flex;
    gap: 10px;
    max-width: 350px;
    margin: ${theme.spacing.lg} auto;
`;

export const Input = styled.input`
    flex: 1;
    padding: ${theme.spacing.sm};
    font-size: ${theme.typography.fontSizes.medium};
    border: 2px solid ${theme.colors.border};
    border-radius: 4px;
    text-transform: uppercase;
    
    &:disabled {
        background-color: ${theme.colors.background.tertiary};
        cursor: not-allowed;
    }
`;

export const Button = styled.button`
    padding: ${theme.spacing.sm} ${theme.spacing.lg};
    font-size: ${theme.typography.fontSizes.medium};
    background-color: ${theme.colors.primary};
    color: ${theme.colors.background.primary};
    border: none;
    border-radius: 4px;
    cursor: pointer;
    
    &:disabled {
        background-color: #cccccc;
        cursor: not-allowed;
    }
    
    &:hover:not(:disabled) {
        background-color: ${theme.colors.primaryHover};
    }
`;

export const ErrorMessage = styled.div`
    color: red;
    margin-top: ${theme.spacing.xs};
`; 