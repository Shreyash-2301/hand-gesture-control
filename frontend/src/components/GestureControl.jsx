import { useState, useEffect, useRef } from 'react';
import {
  Box,
  Grid,
  VStack,
  Heading,
  Text,
  Badge,
  useToast,
  Button,
  HStack,
  Select,
} from '@chakra-ui/react';
import Webcam from 'react-webcam';
import { io } from 'socket.io-client';

const GestureControl = () => {
  const webcamRef = useRef(null);
  const [mode, setMode] = useState('normal');
  const [currentGesture, setCurrentGesture] = useState('None');
  const [isConnected, setIsConnected] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const toast = useToast();
  const socketRef = useRef(null);

  useEffect(() => {
    // Connect to Python backend
    socketRef.current = io('http://localhost:5000');

    socketRef.current.on('connect', () => {
      setIsConnected(true);
      toast({
        title: 'Connected to server',
        status: 'success',
        duration: 2000,
      });
    });

    socketRef.current.on('gesture_detected', (data) => {
      setCurrentGesture(data.gesture);
    });

    socketRef.current.on('disconnect', () => {
      setIsConnected(false);
      toast({
        title: 'Disconnected from server',
        status: 'error',
        duration: 2000,
      });
    });

    return () => {
      if (socketRef.current) {
        socketRef.current.disconnect();
      }
    };
  }, []);

  const handleModeChange = (newMode) => {
    setMode(newMode);
    socketRef.current?.emit('change_mode', { mode: newMode });
  };

  const toggleRecording = () => {
    setIsRecording(!isRecording);
    if (!isRecording) {
      toast({
        title: 'Recording gesture...',
        description: 'Make a gesture and press stop when ready',
        status: 'info',
        duration: null,
      });
    }
  };

  return (
    <Grid templateColumns={{ base: '1fr', md: 'repeat(2, 1fr)' }} gap={8}>
      <VStack spacing={4} align="stretch">
        <Box
          borderWidth={2}
          borderRadius="lg"
          borderColor={isConnected ? 'green.500' : 'red.500'}
          p={4}
        >
          <Webcam
            ref={webcamRef}
            mirrored
            style={{ width: '100%', borderRadius: '8px' }}
          />
        </Box>

        <HStack spacing={4}>
          <Select value={mode} onChange={(e) => handleModeChange(e.target.value)}>
            <option value="normal">Normal Mode</option>
            <option value="mouse">Mouse Control</option>
            <option value="volume">Volume Control</option>
            <option value="drawing">Drawing Mode</option>
          </Select>

          <Button
            colorScheme={isRecording ? 'red' : 'blue'}
            onClick={toggleRecording}
          >
            {isRecording ? 'Stop Recording' : 'Record Gesture'}
          </Button>
        </HStack>
      </VStack>

      <VStack spacing={6} align="stretch">
        <Box p={6} borderWidth={1} borderRadius="lg">
          <Heading size="md" mb={4}>
            Current Status
          </Heading>
          <VStack align="stretch" spacing={3}>
            <HStack justify="space-between">
              <Text>Connection:</Text>
              <Badge colorScheme={isConnected ? 'green' : 'red'}>
                {isConnected ? 'Connected' : 'Disconnected'}
              </Badge>
            </HStack>
            <HStack justify="space-between">
              <Text>Mode:</Text>
              <Badge colorScheme="blue">{mode}</Badge>
            </HStack>
            <HStack justify="space-between">
              <Text>Current Gesture:</Text>
              <Badge colorScheme="purple">{currentGesture}</Badge>
            </HStack>
          </VStack>
        </Box>

        <Box p={6} borderWidth={1} borderRadius="lg">
          <Heading size="md" mb={4}>
            Mode Instructions
          </Heading>
          {mode === 'normal' && (
            <VStack align="stretch" spacing={2}>
              <Text>• Open Palm: Spotlight search</Text>
              <Text>• Closed Fist: Close window</Text>
              <Text>• 2 Fingers: App switcher</Text>
              <Text>• 3 Fingers: Minimize window</Text>
              <Text>• 4 Fingers: Quit application</Text>
            </VStack>
          )}
          {mode === 'mouse' && (
            <VStack align="stretch" spacing={2}>
              <Text>• Move index finger to control cursor</Text>
              <Text>• Pinch (thumb + index) to click</Text>
            </VStack>
          )}
          {mode === 'volume' && (
            <VStack align="stretch" spacing={2}>
              <Text>• Thumb-pinky distance controls volume</Text>
              <Text>• Further apart = Volume up</Text>
              <Text>• Closer together = Volume down</Text>
            </VStack>
          )}
          {mode === 'drawing' && (
            <VStack align="stretch" spacing={2}>
              <Text>• Use index finger to draw</Text>
              <Text>• Press 'c' to change colors</Text>
              <Text>• Press 'x' to clear canvas</Text>
            </VStack>
          )}
        </Box>
      </VStack>
    </Grid>
  );
};

export default GestureControl;