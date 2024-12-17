class AxiosError extends Error {
    constructor(message, response) {
        super(message);
        this.name = 'AxiosError';
        this.response = response;
    }
}

export default AxiosError;