import { useRef } from 'react';
import { toast } from 'react-toastify';

/**
 * useColdStartToast
 * Wraps an async function to show a cold start toast if it takes longer than 2 seconds.
 *
 * Usage:
 *   const runWithColdStartToast = useColdStartToast();
 *   await runWithColdStartToast(() => myAsyncFunc(...args));
 */
export function useColdStartToast() {
    const timeoutRef = useRef<NodeJS.Timeout | null>(null);
    const toastId = 'cold-start-info';

    async function runWithColdStartToast<T>(asyncFn: () => Promise<T>): Promise<T> {
        let toastShown = false;
        
        toast.dismiss(toastId);
        timeoutRef.current = setTimeout(() => {
            toast.info(
                'The backend server is waking up after inactivity. Please be patient as this may take a few moments.',
                { toastId }
            );
            toastShown = true;
        }, 2000);
        try {
            return await asyncFn();
        } finally {
            if (timeoutRef.current) clearTimeout(timeoutRef.current);
            
            // Dismiss toast immediately after completion:
            if (toastShown) toast.dismiss(toastId);
        }
    }


    return runWithColdStartToast;
} 