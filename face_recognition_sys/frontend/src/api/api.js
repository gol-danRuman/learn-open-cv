const sendPhoto = async (file) => {
    const formData = new FormData();
    formData.append('photo', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/verify', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to send photo');
      }

      const data = await response.json();
      console.log('Photo upload successful:', data);
    } catch (error) {
      console.error('Error sending photo:', error);
    }
  };