# Copyright (c) 2018, The Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of the University of California nor the
#   names of its contributors may be used to endorse or promote products
#   derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OF THE UNIVERSITY OF CALIFORNIA
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import unittest

from cogrob.dialogue.intent import hypothesis_pb2
from cogrob.dialogue.intent_extractors import quiz_extractor

class TestIntents(unittest.TestCase):
  def setUp(self):
    self._extractor = quiz_extractor.QuizExtractor()


  def testWhiteHouse(self):
    input = hypothesis_pb2.IntentHypothesisMetadata()
    input.source_transcript = "white house"
    output = []
    self._extractor.Extract(input, output.append)
    output = filter(lambda x: x.metadata.confidence_score > 0.7, output)
    output = filter(
        lambda x: x.intent.quiz_answer.matched_answer == "white_house", output)
    self.assertGreater(len(output), 0)


  def testWrongAnswerHotAir(self):
    input = hypothesis_pb2.IntentHypothesisMetadata()
    input.source_transcript = "heavier"
    output = []
    self._extractor.Extract(input, output.append)
    output = filter(lambda x: x.metadata.confidence_score > 0.7, output)
    output = filter(
        lambda x: x.intent.quiz_answer.matched_wrong_answer == "hot_air",
        output)
    self.assertGreater(len(output), 0)


  def testNothing(self):
    input = hypothesis_pb2.IntentHypothesisMetadata()
    input.source_transcript = "balalalal"
    output = []
    self._extractor.Extract(input, output.append)
    output = filter(lambda x: x.metadata.confidence_score > 0.7, output)
    self.assertEqual(len(output), 0)


if __name__ == '__main__':
  unittest.main()
