import React from 'react';
import {Composition} from 'remotion';
import {Cena, DURACAO, FPS} from './Cena';
export const Root: React.FC = () => (
  <Composition id="Banca" component={Cena} durationInFrames={DURACAO} fps={FPS} width={1080} height={1920} />
);
