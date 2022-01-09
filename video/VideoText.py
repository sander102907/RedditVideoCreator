import cv2
import numpy as np
from copy import copy

class VideoText:
    @staticmethod
    def draw_text(
        frame,
        text,
        complete_text,
        center=True,
        color=(255, 255, 255),
        fontScale=0.5,
        thickness=1,
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        outline_color=(0, 0, 0),
        line_spacing=1.5,
    ) -> np.ndarray:
        """
        Draws multiline with an outline.
        """
        assert isinstance(text, str)

        margin = 50
        width = len(frame[0]) - (margin * 2)

        lines = VideoText.__get_lines(text, fontFace, fontScale, thickness, width)
        all_lines = VideoText.__get_lines(complete_text, fontFace, fontScale, thickness, width)

        if center:
            line_height = lines[0][1]
            text_height = line_height * len(all_lines) * line_spacing
            middle = len(frame) / 2
            top = middle - (text_height / 2)
            uv_top_left = np.array([margin, top], dtype=float)
        else:
            uv_top_left = np.array([margin, margin], dtype=float)

        for line in lines:
            text, h = line
            uv_bottom_left_i = uv_top_left + [0, h]
            org = tuple(uv_bottom_left_i.astype(int))

            if outline_color is not None:
                cv2.putText(
                    frame,
                    text=text,
                    org=org,
                    fontFace=fontFace,
                    fontScale=fontScale,
                    color=outline_color,
                    thickness=thickness * 3,
                    lineType=cv2.LINE_AA,
                )
            cv2.putText(
                frame,
                text=text,
                org=org,
                fontFace=fontFace,
                fontScale=fontScale,
                color=color,
                thickness=thickness,
                lineType=cv2.LINE_AA,
            )

            uv_top_left += [0, h * line_spacing]

        return frame


    @staticmethod
    def __get_lines(text, fontFace, fontScale, thickness, width):
        inp_lines = text.splitlines()
        out_lines = []

        for line in inp_lines:
            while len(line.strip()) > 0:
                (w, h), _ = cv2.getTextSize(
                    text=line,
                    fontFace=fontFace,
                    fontScale=fontScale,
                    thickness=thickness,
                )

                tmp_line = copy(line)

                while w > width:
                    tmp_line = ' '.join(tmp_line.split(' ')[:-1])
                    (w, h), _ = cv2.getTextSize(
                        text=tmp_line,
                        fontFace=fontFace,
                        fontScale=fontScale,
                        thickness=thickness,
                    )

                out_lines.append((tmp_line, h))
                line = ' '.join(line.split(' ')[len(tmp_line.split(' ')):])
                                    
        return out_lines


