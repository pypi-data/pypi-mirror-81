# -*- coding: utf-8 -*-

# This file is part of Kaleidoscope.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable=unexpected-keyword-arg

"""Module for easily getting IBMQ systems"""

import warnings
from ._account import Account


class KaleidoscopeSystemService():
    """The service class for systems.

    All attributes are dynamically attached to
    this class.

    This class is much simpler than the simulators
    one because there is no processing that needs
    to be done async.
    """

    def __init__(self):
        self._all_added_attr = None
        self._default_added_attr = None
        self._default_provider = Account.get_default_provider()
        _system_loader(self)

    def __call__(self):
        return list(vars(self).keys())

    def _refresh(self):
        """Refresh the service in place.
        """
        for key in self._default_added_attr:
            try:
                del self.__dict__[key]
            except AttributeError:
                pass
        self._all_added_attr = []
        self._default_added_attr = []
        self._default_provider = Account.get_default_provider()
        if hasattr(self, 'OTHER'):
            delattr(self, 'OTHER')
        _system_loader(self)


class KaleidoscopeSystemDispatcher():
    """Contains all the backend instances
    corresponding to the providers for a given
    system.

    All attributes are dynamically attached to
    this class.
    """
    def __call__(self):
        return list(vars(self).keys())


def _system_loader(service):
    """Attaches system dispatchers to the service
    """
    if not any(Account.providers()):
        try:
            Account.load_account()
        except Exception:  # pylint: disable=broad-except
            pass
    systems = _get_ibmq_systems()
    all_added_attr = []
    default_added_attr = []
    default_provider = service._default_provider.split('//') if service._default_provider else []

    num_providers = len(Account.providers())
    if num_providers > 1:
        setattr(service, 'OTHER', KaleidoscopeSystemDispatcher())
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for name, back_list in systems.items():
            reference = back_list[0]
            num_qubits = reference._configuration.num_qubits
            system_name = "{}𖼯{}Q𖼞".format(name, num_qubits)
            all_dispatcher = KaleidoscopeSystemDispatcher()
            for backend in back_list:
                hub = backend.hub
                group = backend.group
                project = backend.project
                max_shots = backend._configuration.max_shots
                max_circuits = backend._configuration.max_experiments
                pulse = '_P' if backend._configuration.open_pulse else ''
                pro_str = "𖼯{}_{}{}𖼞{}_{}_{}".format(max_circuits, max_shots, pulse,
                                                     hub, group, project)
                pro_str = pro_str.replace('-', 'ー')
                setattr(all_dispatcher, pro_str, backend)
                # is backend in default provider
                if [hub, group, project] == default_provider:
                    setattr(service, system_name, backend)
                    default_added_attr.append(system_name)

            if num_providers > 1:
                setattr(service.OTHER, 'get_'+system_name, all_dispatcher)
            all_added_attr.append(system_name)

    service._all_added_attr = all_added_attr
    service._default_added_attr = default_added_attr


def _get_ibmq_systems():
    """Get instances for all IBMQ systems that the user has access to.

    Returns:
        dict: A dict of all IBMQ systems that a user has access to.
    """
    ibmq_backends = {}
    for pro in Account.providers():
        for back in pro.backends():
            if not back.configuration().simulator:
                if ('alt' not in back.name()) \
                        and back.name().startswith('ibmq'):
                    if back.name() not in ibmq_backends:
                        ibmq_backends[back.name()] = [back]
                    else:
                        ibmq_backends[back.name()].append(back)
    return ibmq_backends
