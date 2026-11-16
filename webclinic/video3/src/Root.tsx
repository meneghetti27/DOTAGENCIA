import React from 'react';
import {Composition} from 'remotion';
import {Video, DURACAO} from './Video';
export const Root: React.FC = () => (
  <Composition id="Apresentacao" component={Video} durationInFrames={DURACAO} fps={30} width={1080} height={1920} />
);
