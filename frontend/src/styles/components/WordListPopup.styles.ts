import styled from '@emotion/styled';
import { theme } from '../theme';

export const Overlay = styled.div`
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: ${theme.colors.background.overlay};
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
`;

export const PopupContent = styled.div`
    background-color: ${theme.colors.background.primary};
    padding: ${theme.spacing.lg};
    border-radius: 8px;
    max-width: 90%;
    width: 500px;
    max-height: 80vh;
    position: relative;
    box-shadow: ${theme.shadows.md};
`;

export const CloseButton = styled.button`
    position: absolute;
    top: ${theme.spacing.sm};
    right: ${theme.spacing.sm};
    background: none;
    border: none;
    font-size: ${theme.typography.fontSizes.xlarge};
    cursor: pointer;
    color: #666;
    
    &:hover {
        color: #333;
    }
`;

export const Title = styled.h2`
    margin-top: 0;
    margin-bottom: ${theme.spacing.lg};
    color: ${theme.colors.text.primary};
    font-size: ${theme.typography.fontSizes.large};
`;

export const WordList = styled.div`
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: ${theme.spacing.sm};
    max-height: calc(80vh - 100px);
    overflow-y: auto;
    padding: ${theme.spacing.sm};
    
    &::-webkit-scrollbar {
        width: 8px;
    }
    
    &::-webkit-scrollbar-track {
        background: ${theme.colors.background.secondary};
        border-radius: 4px;
    }
    
    &::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }
`;

export const Word = styled.div`
    padding: ${theme.spacing.xs};
    background-color: ${theme.colors.background.secondary};
    border-radius: 4px;
    text-align: center;
    font-family: monospace;
    color: ${theme.colors.primaryHover};
`; 