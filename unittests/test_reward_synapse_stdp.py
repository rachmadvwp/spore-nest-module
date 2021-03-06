#! /usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is part of SPORE.
#
# Copyright (C) 2016, the SPORE team (see AUTHORS).
#
# SPORE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# SPORE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SPORE.  If not, see <http://www.gnu.org/licenses/>.
#
# For more information see: https://github.com/IGITUGraz/spore-nest-module
#

import numpy as np
import nest
import unittest


class TestStringMethods(unittest.TestCase):

    # test connection
    def spore_connection_test(self, resolution, interval, delay, exp_len):

        spike_times_in = [10.0, 15.0, 20.0, 25.0, 50.0]
        spike_times_out = [40.0, 50.0, 60.0, 70.0]

        synapse_properties = {"weight_update_interval": 100.0, "temperature": 0.0,
                              "synaptic_parameter": 1.0, "reward_transmitter": None,
                              "learning_rate": 0.0001, "episode_length": 100.0,
                              "max_param": 100.0, "min_param": -100.0, "max_param_change": 100.0,
                              "integration_time": 10000.0}

        nest.ResetKernel()
        nest.SetKernelStatus({"resolution": resolution})
        nest.sli_func("InitSynapseUpdater", interval, delay)
        nest.CopyModel("spore_test_node", "test_pulse_trace", {"test_name": "test_pulse_trace",
                                                               "spike_times": np.array(spike_times_out),
                                                               "weight": 1.0,
                                                               "offset": -0.2})

        # Create spike generators and connect
        gin = nest.Create("spike_generator",  params={"spike_times": np.array(spike_times_in)})
        nout = nest.Create("test_pulse_trace")

        nodes = nest.Create("test_pulse_trace", 1)
        nest.CopyModel("synaptic_sampling_rewardgradient_synapse", "test_synapse")
        synapse_properties["reward_transmitter"] = nodes[0]
        nest.SetDefaults("test_synapse", synapse_properties)
        nest.Connect([gin[0]], [nout[0]], "one_to_one", {"model": "test_synapse"})
        conns = nest.GetConnections([gin[0]], [nout[0]], "test_synapse")
        nest.SetStatus(conns, {"recorder_interval": 100.0})

        nest.Simulate(exp_len)

        results = nest.GetStatus(conns, ["recorder_times", "synaptic_parameter_values"])

        times = [0.0, 100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0,
                 1100.0, 1200.0, 1300.0, 1400.0, 1500.0, 1600.0, 1700.0, 1800.0, 1900.0,
                 2000.0, 2100.0, 2200.0, 2300.0, 2400.0, 2500.0, 2600.0, 2700.0, 2800.0,
                 2900.0, 3000.0, 3100.0, 3200.0, 3300.0, 3400.0, 3500.0, 3600.0, 3700.0,
                 3800.0, 3900.0, 4000.0, 4100.0, 4200.0, 4300.0, 4400.0, 4500.0, 4600.0,
                 4700.0, 4800.0, 4900.0, 5000.0, 5100.0, 5200.0, 5300.0, 5400.0, 5500.0,
                 5600.0, 5700.0, 5800.0, 5900.0, 6000.0, 6100.0, 6200.0, 6300.0, 6400.0,
                 6500.0, 6600.0, 6700.0, 6800.0, 6900.0, 7000.0, 7100.0, 7200.0, 7300.0,
                 7400.0, 7500.0, 7600.0, 7700.0, 7800.0, 7900.0, 8000.0, 8100.0, 8200.0,
                 8300.0, 8400.0, 8500.0, 8600.0, 8700.0, 8800.0, 8900.0, 9000.0, 9100.0,
                 9200.0, 9300.0, 9400.0, 9500.0, 9600.0, 9700.0, 9800.0, 9900.0]

        values = [1.0, 1.1941197605580636, 1.5774259143750948, 2.0259103145644266, 2.4921365591257456,
                  2.9587360738461674, 3.4194121087993565, 3.871939771677826, 4.315590899450609, 4.750186736885722,
                  5.175749451568903, 5.592373948376652, 6.000180727410171, 6.399298555975304, 6.789858108361998,
                  7.171989640278706, 7.545822147382392, 7.911483069607812, 8.269098196118081, 8.618791643894623,
                  8.960685863254373, 9.29490165311173, 9.621558179666037, 9.940772996191743, 10.252662063078569,
                  10.557339767809804, 10.854918944765805, 11.14551089481294, 11.429225404665099, 11.706170766014766,
                  11.976453794434303, 12.240179848049316, 12.497452845986553, 12.748375286598817, 12.993048265469508,
                  13.231571493199345, 13.464043312977822, 13.690560717941914, 13.91121936832454, 14.126113608395242,
                  14.33533648319552, 14.53897975507124, 14.737133920004482, 14.929888223747206, 15.11733067775905,
                  15.299548074951568, 15.476626005241176, 15.64864887091307, 15.815699901798324, 15.97786117026638,
                  16.13521360603509, 16.287837010800473, 16.43581007268829, 16.579210380529563, 16.71811443796208,
                  16.852597677359963, 16.982734473593325, 17.10859815762, 17.230261029911343, 17.34779437371405,
                  17.461268468149946, 17.570752601155647, 17.67631508226397, 17.778023255228995, 17.875943510496594,
                  17.97014129752227, 18.06068113693813, 18.147626632570702, 18.23104048331149, 18.31098449484185,
                  18.38751959121408, 18.46070582629026, 18.530602395040663, 18.597267644703344, 18.66075908580651,
                  18.721133403055404, 18.778446466085196, 18.832753340081556, 18.884108296270426, 18.93256482227858,
                  18.978175632366465, 19.0209926775349, 19.061067155507057, 19.098449520587284, 19.133189493398152,
                  19.165336070497265, 19.194937533875176, 19.222041460335888, 19.24669473076129, 19.268943539260974,
                  19.288833402208706, 19.306409167166986, 19.321715021701, 19.33479450208325, 19.345690501890225,
                  19.35444528049237, 19.361100471438604, 19.365697090736695, 19.3682755450307, 19.368875639676705]

        self.assertAlmostEqual(np.sum((np.array(results[0][0]) - np.array(times))**2), 0.0)
        self.assertAlmostEqual(np.sum((np.array(results[0][1]) - np.array(values))**2), 0.0)

    def test_reward_synapse(self):
        self.spore_connection_test(1.0, 100, 100, 10000.0)


if __name__ == '__main__':
    nest.Install("sporemodule")
    unittest.main()
