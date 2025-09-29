"""Demonstrates molecular dynamics with constant energy."""

from ase import units
from ase.lattice.cubic import FaceCenteredCubic
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from asap3 import Trajectory

def calcenergy(a):
    epot = a.get_potential_energy() / len(a)
    ekin = a.get_kinetic_energy() / len(a)
    etot = epot + ekin
    temp = 2/3*ekin*1/units.kB

    return epot, ekin, etot, temp



def run_md():
    # Use Asap for a huge performance increase if it is installed
    use_asap = True

    if use_asap:
        from asap3 import EMT

        size = 10
    else:
        from ase.calculators.emt import EMT

        size = 3

    # Set up a crystal
    atoms = FaceCenteredCubic(
        directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        symbol='Cu',
        size=(size, size, size),
        pbc=True,
    )

    # Describe the interatomic interactions with the Effective Medium Theory
    atoms.calc = EMT()

    # Set the momenta corresponding to T=300K
    MaxwellBoltzmannDistribution(atoms, temperature_K=300)

    # We want to run MD with constant energy using the VelocityVerlet algorithm.
    dyn = VelocityVerlet(atoms, 5 * units.fs)  # 5 fs time step.

    traj = Trajectory("cu.traj","w",atoms)
    dyn.attach(traj.write, interval=10) #Kommer var tioende iteration spara till "cu.traj" fil


    def printenergy(a=atoms):  # store a reference to atoms in the definition.
        """Function to print the potential, kinetic and total energy."""
        epot, ekin, etot, temp = calcenergy(a)
        print(
            f'Energy per atom: Epot ={epot:6.3f}eV  Ekin = {ekin:.3f}eV '
            f'(T={temp:3.0f}K) Etot = {etot:.3f}eV'
        )


    # Now run the dynamics
    dyn.attach(printenergy, interval=10) #Vid varje tionde iteration, kalla printenergy
    printenergy() #Kallar 1 gång innan vi börjar, så start energin.
    dyn.run(200)


    """
    "cu.traj" saves snapshots of the atoms during the simulation.

    Nows position etc. Velocities.

    Doing "gui ase cu.traj" re-creates atoms objects from all these snapshots.
    This is what allows us to animate the movement.

    We never explciitly save energy information, but these new objects know what calculator
    the original object we simulated used.
    Hence, using information that we stored, it re-calculates energies.

    And thats why we also get an energy plot, even tough we never explicitly saved that.

    """
if __name__ == "__main__":
    run_md()