import { fetchAnswer } from './Ask';

global.fetch = jest.fn();

describe('fetchAnswer', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  it('should return the answer from the backend', async () => {
    fetch.mockResolvedValueOnce({
      json: async () => ({ answer: 'ICS 31 is manageable.' }),
    });

    const result = await fetchAnswer('Is ICS 31 hard?');
    expect(result).toBe('ICS 31 is manageable.');
  });

  it('should handle empty responses', async () => {
    fetch.mockResolvedValueOnce({
      json: async () => ({}),
    });

    const result = await fetchAnswer('Is ICS 32 easy?');
    expect(result).toBe('No answer returned.');
  });

  it('should return error message on fetch failure', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'));

    const result = await fetchAnswer('Hello?');
    expect(result).toBe('Something went wrong.');
  });
});
