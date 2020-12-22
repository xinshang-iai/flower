# Copyright 2020 Adap GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""FedAdagrad tests."""


from typing import List, Optional, Tuple
from unittest.mock import MagicMock

from numpy import array, float32

from flwr.common import (
    EvaluateRes,
    FitIns,
    FitRes,
    Parameters,
    Weights,
    weights_to_parameters,
)
from flwr.server.client_proxy import ClientProxy
from flwr.server.grpc_server.grpc_client_proxy import GrpcClientProxy

from .fedadagrad import FedAdagrad


def test_aggregate_fit() -> None:
    # Prepare
    strategy = FedAdagrad(eta=0.1, eta_l=0.316, tau=0.5)
    param_0: Parameters = weights_to_parameters(
        [array([0.2, 0.2, 0.2, 0.2], dtype=float32)]
    )
    param_1: Parameters = weights_to_parameters(
        [array([1.0, 1.0, 1.0, 1.0], dtype=float32)]
    )
    bridge = MagicMock()
    client_0 = GrpcClientProxy(cid="0", bridge=bridge)
    client_1 = GrpcClientProxy(cid="1", bridge=bridge)
    results: List[Tuple[ClientProxy, FitRes]] = [
        (
            client_0,
            FitRes(param_0, num_examples=5, num_examples_ceil=5, fit_duration=0.1),
        ),
        (
            client_1,
            FitRes(param_1, num_examples=5, num_examples_ceil=5, fit_duration=0.1),
        ),
    ]
    previous_weights: Weights = [array([0.1, 0.1, 0.1, 0.1], dtype=float32)]
    expected: Weights = [array([0.15, 0.15, 0.15, 0.15], dtype=float32)]

    # Execute
    actual_list = strategy.aggregate_fit(
        rnd=1, results=results, failures=[], previous_weights=previous_weights
    )
    if actual_list:
        actual = actual_list[0]
    assert (actual == expected[0]).all()
