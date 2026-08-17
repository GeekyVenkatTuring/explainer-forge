import React from "react";
import { CalculateMetadataFunction, Composition } from "remotion";
import { Explainer, ExplainerProps } from "./Explainer";
import { ThumbCard } from "./Thumb";
import { VShort, ShortProps } from "./VShort";

const calculateMetadata: CalculateMetadataFunction<ExplainerProps> = async ({ props }) => {
  const cuts = props.cuts || [];
  if (cuts.length === 0) return { durationInFrames: 30 * 60 };
  const lastEnd = Math.max(...cuts.map((c) => c.out_seconds || 0));
  return { durationInFrames: Math.ceil((lastEnd + 1) * 30) }; // +1s tail for final fade
};

export const Root: React.FC = () => (
  <>
    <Composition
      id="Explainer"
      component={Explainer}
      durationInFrames={30 * 60}
      fps={30}
      width={1920}
      height={1080}
      defaultProps={{ cuts: [], audio: {} }}
      calculateMetadata={calculateMetadata}
    />
    <Composition
      id="ExplainerVertical"
      component={Explainer}
      durationInFrames={30 * 60}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{ cuts: [], audio: {} }}
      calculateMetadata={calculateMetadata}
    />
    <Composition
      id="Thumbnail"
      component={ThumbCard}
      durationInFrames={1}
      fps={30}
      width={1280}
      height={720}
      defaultProps={{}}
    />
    <Composition
      id="Short"
      component={VShort}
      durationInFrames={30 * 20}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{}}
      calculateMetadata={async ({ props }: { props: ShortProps }) => ({
        durationInFrames: Math.ceil((props.durationSec || 20) * 30),
      })}
    />
  </>
);
