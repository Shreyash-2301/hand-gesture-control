import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import GestureControl from './components/GestureControl';
import MouseControl from './components/MouseControl';
import VolumeControl from './components/VolumeControl';
import DrawingMode from './components/DrawingMode';

const AppRoutes = () => {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<GestureControl />} />
        <Route path="/mouse-control" element={<MouseControl />} />
        <Route path="/volume-control" element={<VolumeControl />} />
        <Route path="/drawing" element={<DrawingMode />} />
      </Routes>
    </Layout>
  );
};

export default AppRoutes;