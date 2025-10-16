import {
  Box,
  Flex,
  IconButton,
  useColorMode,
  useColorModeValue,
  Container,
  Heading,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Text,
} from '@chakra-ui/react';
import {
  FiMenu,
  FiMoon,
  FiSun,
  FiVideo,
  FiMousePointer,
  FiVolume2,
  FiEdit,
} from 'react-icons/fi';
import { Link } from 'react-router-dom';

function Layout({ children }) {
  const { colorMode, toggleColorMode } = useColorMode();
  const bg = useColorModeValue('white', 'gray.800');
  const color = useColorModeValue('gray.800', 'white');

  return (
    <Box minH="100vh" bg={useColorModeValue('gray.50', 'gray.900')}>
      <Flex
        as="nav"
        align="center"
        justify="space-between"
        wrap="wrap"
        padding={4}
        bg={bg}
        color={color}
        boxShadow="sm"
      >
        <Flex align="center" mr={5}>
          <Link to="/">
            <Heading as="h1" size="lg" letterSpacing={'tighter'}>
              Gesture Control
            </Heading>
          </Link>
        </Flex>

        <Flex align="center">
          <Menu>
            <MenuButton
              as={IconButton}
              aria-label="Menu"
              icon={<FiMenu />}
              variant="ghost"
              mr={2}
            />
            <MenuList>
              <MenuItem as={Link} to="/" icon={<FiVideo />}>
                Gesture Demo
              </MenuItem>
              <MenuItem as={Link} to="/mouse-control" icon={<FiMousePointer />}>
                Mouse Control
              </MenuItem>
              <MenuItem as={Link} to="/volume-control" icon={<FiVolume2 />}>
                Volume Control
              </MenuItem>
              <MenuItem as={Link} to="/drawing" icon={<FiEdit />}>
                Drawing Mode
              </MenuItem>
            </MenuList>
          </Menu>

          <IconButton
            icon={colorMode === 'light' ? <FiMoon /> : <FiSun />}
            onClick={toggleColorMode}
            variant="ghost"
          />
        </Flex>
      </Flex>

      <Container maxW="container.xl" py={8}>
        {children}
      </Container>

      <Box as="footer" py={4} textAlign="center">
        <Text>© 2025 Gesture Control. All rights reserved.</Text>
      </Box>
    </Box>
  );
}

export default Layout;