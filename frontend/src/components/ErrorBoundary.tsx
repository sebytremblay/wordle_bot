import React, { Component, ErrorInfo, ReactNode } from 'react';
import styled from 'styled-components';

const ErrorContainer = styled.div`
    padding: 20px;
    margin: 20px;
    border: 1px solid ${props => props.theme.colors.error};
    border-radius: 4px;
    color: ${props => props.theme.colors.error};
`;

const ErrorMessage = styled.p`
    margin: 10px 0;
    font-size: 1rem;
`;

const RetryButton = styled.button`
    padding: 8px 16px;
    background-color: ${props => props.theme.colors.primary};
    color: ${props => props.theme.colors.white};
    border: none;
    border-radius: 4px;
    cursor: pointer;
    
    &:hover {
        background-color: ${props => props.theme.colors.primaryDark};
    }
`;

interface Props {
    children: ReactNode;
}

interface State {
    hasError: boolean;
    error: Error | null;
}

class ErrorBoundary extends Component<Props, State> {
    public state: State = {
        hasError: false,
        error: null,
    };

    public static getDerivedStateFromError(error: Error): State {
        return {
            hasError: true,
            error,
        };
    }

    public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        console.error('Uncaught error:', error, errorInfo);
    }

    private handleRetry = () => {
        this.setState({ hasError: false, error: null });
    };

    public render() {
        if (this.state.hasError) {
            return (
                <ErrorContainer>
                    <h2>Something went wrong</h2>
                    <ErrorMessage>
                        {this.state.error?.message || 'An unexpected error occurred'}
                    </ErrorMessage>
                    <RetryButton onClick={this.handleRetry}>
                        Try Again
                    </RetryButton>
                </ErrorContainer>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary; 