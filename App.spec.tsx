import React from 'react';

describe('<App />', () => {
  it('intentional failure for AI to fix', () => {
    const x: number = 5;
    // The AI must change this to 5 to pass
    expect(x).toBe(10); 
  });
});
