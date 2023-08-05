from typing import (
    Dict,
    List,
    TypeVar,
)
from ..virtualmachine import VirtualMachine, VirtualMachineState

TCachingDiskStateFetcher = TypeVar("TCachingDiskStateFetcher", bound="CachingMachine")


class CachingVirtualMachine(VirtualMachine):
    def __init__(self, fetcher: TCachingDiskStateFetcher, id: int) -> None:
        super().__init__(id=id)
        self._fetcher = fetcher
        self._cached_state = self._state

    async def start(self, overcommit: bool = False) -> bool:
        """Starts a stopped virtual machine."""
        return await self._fetcher._start_vm(self, overcommit)

    async def stop(self, force: bool = False) -> bool:
        """Stops a running virtual machine."""
        return await self._fetcher._stop_vm(self, force)

    async def restart(self) -> bool:
        """Restarts a running virtual machine."""
        return await self._fetcher._restart_vm(self)

    @property
    def available(self) -> bool:
        """If the virtual machine exists on the server."""
        return self._id in self._fetcher._state

    @property
    def description(self) -> str:
        """The description of the virtual machine."""
        if self.available:
            self._cached_state = self._state
            return self._state["description"]
        return self._cached_state["description"]

    @property
    def name(self) -> str:
        """The name of the virtual machine."""
        if self.available:
            self._cached_state = self._state
            return self._state["name"]
        return self._cached_state["name"]

    @property
    def status(self) -> VirtualMachineState:
        """The status of the virtual machine."""
        assert self.available
        return VirtualMachineState.fromValue(self._state["status"]["state"])

    @property
    def _state(self) -> dict:
        """The state of the virtual machine, according to the Machine."""
        return self._fetcher._get_cached_state(self)


class CachingVirtualMachineStateFetcher(object):
    _parent: TCachingDiskStateFetcher
    _state: Dict[str, dict]
    _cached_vms: List[CachingVirtualMachine]

    def __init__(self, machine: TCachingDiskStateFetcher) -> None:
        self._parent = machine
        self._state = {}
        self._cached_vms = []

    async def get_vms(self) -> List[CachingVirtualMachine]:
        """Returns a list of virtual machines on the host."""
        self._state = await self._fetch_vms()
        self._update_properties_from_state()
        return self.vms

    @property
    def vms(self) -> List[VirtualMachine]:
        """Returns a list of virtual machines on the host."""
        return self._cached_vms

    async def _start_vm(self, vm: VirtualMachine, overcommit: bool = False) -> bool:
        assert self._parent._client is not None
        return await self._parent._client.invoke_method(
            "vm.start", [vm.id, {"overcommit": overcommit}],
        )

    async def _stop_vm(self, vm: VirtualMachine, force: bool = False) -> bool:
        assert self._parent._client is not None
        return await self._parent._client.invoke_method("vm.stop", [vm.id, force])

    async def _restart_vm(self, vm: VirtualMachine) -> bool:
        assert self._parent._client is not None
        return await self._parent._client.invoke_method("vm.restart", [vm.id])

    def _get_cached_state(self, vm: VirtualMachine) -> dict:
        return self._state[vm.id]

    async def _fetch_vms(self) -> Dict[str, dict]:
        assert self._parent._client is not None
        vms = await self._parent._client.invoke_method(
            "vm.query", [[], {"select": ["id", "name", "description", "status",],},],
        )
        return {vm["id"]: vm for vm in vms}

    def _update_properties_from_state(self) -> None:
        available_vms_by_id = {vm.id: vm for vm in self._cached_vms if vm.available}
        current_vm_ids = {vm_id for vm_id in self._state}
        vm_ids_to_add = current_vm_ids - set(available_vms_by_id)
        self._cached_vms = [*available_vms_by_id.values()] + [
            CachingVirtualMachine(fetcher=self, id=vm_id) for vm_id in vm_ids_to_add
        ]
