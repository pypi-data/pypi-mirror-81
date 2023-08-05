from __future__ import annotations

from typing import Final

import rumps
from ycontract import contract

from exclock.sound_player import Player


class RumpsApp(rumps.App):

    @contract(lambda maxsec: maxsec > 0)
    def __init__(self, *, clock_title: str, message: str, ring_filename: str, maxsec: int):
        super().__init__(clock_title)
        self.clock_title: Final[str] = clock_title
        self.message: Final[str] = message
        self.ring_filename = ring_filename
        self.t = 0
        self.maxsec: Final[int] = maxsec

    @rumps.timer(1)
    def update_time(self, _):
        self.t += 1
        percent = int(100 * self.t / (self.maxsec))
        self.title = f'{self.clock_title} {self.t} / {self.maxsec} {percent}%'

        if self.t == self.maxsec:
            rumps.notification(message=self.message, title=self.clock_title, subtitle='')
            Player(self.ring_filename).play()
            rumps.quit_application()


if __name__ == '__main__':
    app = RumpsApp(
        clock_title='Rumps Test',
        message='finished',
        maxsec=10,
        ring_filename='./exclock/assets/sound/ring.mp3')
    app.run()
