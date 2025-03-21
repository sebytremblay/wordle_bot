type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface LoggerConfig {
    minLevel: LogLevel;
    enabled: boolean;
}

const LOG_LEVELS: Record<LogLevel, number> = {
    debug: 0,
    info: 1,
    warn: 2,
    error: 3,
};

class Logger {
    private config: LoggerConfig;

    constructor() {
        this.config = {
            minLevel: process.env.NODE_ENV === 'production' ? 'warn' : 'debug',
            enabled: process.env.NODE_ENV !== 'test',
        };
    }

    private shouldLog(level: LogLevel): boolean {
        return (
            this.config.enabled &&
            LOG_LEVELS[level] >= LOG_LEVELS[this.config.minLevel]
        );
    }

    private formatMessage(component: string, message: string): string {
        return `[${component}] ${message}`;
    }

    debug(component: string, message: string, ...args: any[]): void {
        if (this.shouldLog('debug')) {
            console.debug(this.formatMessage(component, message), ...args);
        }
    }

    info(component: string, message: string, ...args: any[]): void {
        if (this.shouldLog('info')) {
            console.info(this.formatMessage(component, message), ...args);
        }
    }

    warn(component: string, message: string, ...args: any[]): void {
        if (this.shouldLog('warn')) {
            console.warn(this.formatMessage(component, message), ...args);
        }
    }

    error(component: string, message: string, ...args: any[]): void {
        if (this.shouldLog('error')) {
            console.error(this.formatMessage(component, message), ...args);
        }
    }
}

export const logger = new Logger(); 