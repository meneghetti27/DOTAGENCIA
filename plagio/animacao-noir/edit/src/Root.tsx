import React from 'react';
import {Composition} from 'remotion';
import {Filme, DURACAO, FPS} from './Filme';
export const Root: React.FC = () => (
  <Composition id="RH" component={Filme} durationInFrames={DURACAO} fps={FPS} width={1080} height={1920} />
);
