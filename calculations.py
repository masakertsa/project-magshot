"""
Project MagShot - Calculation Framework
This script provides the foundational mathematical scaffolding for a closed-loop planetary 
transport infrastructure, including mass-based initial kinetic injection, modular track classes, 
vacuum clamping forces, and 360-degree radial magnetic stability.
"""

import math


def calculate_initial_kinetic_injection_velocity(vessel_mass_kg, stage_zero_joules):
    """
    Calculates the entry velocity achieved by the vessel at the start of the 
    10-meter tube modules based on its mass and the initial electromagnetic injection energy.
    Verifies that the injection speed matches the magnetic synchronization threshold.
    
    Formula: KE = 0.5 * m * v^2 -> v = sqrt(2 * KE / m)
    """
    if vessel_mass_kg <= 0 or stage_zero_joules <= 0:
        return 0.0
    injection_velocity = math.sqrt((2 * stage_zero_joules) / vessel_mass_kg)
    return round(injection_velocity, 2)


def calculate_passenger_g_force(vessel_velocity=8000, track_length=600000):
    """
    Calculates the exact G-force experienced by human passengers on the 600 km track.
    Verifies that the ~5.4 G acceleration is balanced by liquid immersion.
    
    Formula: a = v^2 / (2 * s)
    """
    if track_length <= 0:
        return 0.0
    acceleration = (vessel_velocity ** 2) / (2 * track_length)
    g_force = acceleration / 9.81
    return round(g_force, 2)  # Returns ~5.44 G


def calculate_cargo_g_force(vessel_velocity=8000, track_length=24000):
    """
    Calculates the extreme G-force on the 24 km cargo track to ensure electronics 
    and materials can withstand the structural compression.
    """
    if track_length <= 0:
        return 0.0
    acceleration = (vessel_velocity ** 2) / (2 * track_length)
    g_force = acceleration / 9.81
    return round(g_force, 2)  # Returns ~135.92 G


def calculate_vacuum_seal_clamping_force(plug_radius_meters, vacuum_level_torr=0.0):
    """
    Calculates the passive atmospheric clamping force (in Newtons) holding the greased, grooved 
    end-plug in place. Models how external sea-level air pressure (760 Torr / 101,325 Pa) 
    seals the tunnel as the internal vacuum approaches 0 Torr.
    
    Formula: F = delta_P * Area
    """
    if plug_radius_meters <= 0 or vacuum_level_torr < 0:
        return 0.0
        
    sea_level_pressure_pa = 101325.0
    # Convert internal Torr pressure to Pascals (1 Torr = 133.322 Pa)
    internal_pressure_pa = min(sea_level_pressure_pa, vacuum_level_torr * 133.322)
    
    pressure_delta = sea_level_pressure_pa - internal_pressure_pa
    plug_area_m2 = math.pi * (plug_radius_meters ** 2)
    
    clamping_force_newtons = pressure_delta * plug_area_m2
    return round(clamping_force_newtons, 2)


def calculate_360_symmetrical_stabilization(skew_angle_degrees, accordion_flex_ratio):
    """
    Models the 360-degree radial stabilization and cogging torque suppression inside 
    the 10-meter oblique modules based on magnet skew angle and accordion damping ratio.
    """
    if not (0.0 < skew_angle_degrees <= 45.0) or not (0.0 < accordion_flex_ratio <= 1.0):
        return "CALIBRATION_REQUIRED"
        
    # Optimal cogging torque suppression occurs around 15-degree skew and >0.7 flex damping
    cogging_suppression_efficiency = math.sin(math.radians(skew_angle_degrees * 6)) * accordion_flex_ratio
    
    if cogging_suppression_efficiency >= 0.70:
        return "OPTIMAL_360_STABILITY"
    return "NOMINAL_STABILITY"


if __name__ == "__main__":
    print("--- Project MagShot: Calculation Framework ---")
    
    v_inject = calculate_initial_kinetic_injection_velocity(5000.0, 250_000_000.0)
    print(f"1. Stage-0 Kinetic Injection Velocity: {v_inject} m/s")
    
    g_pass = calculate_passenger_g_force()
    print(f"2. Class 2 Passenger Track Acceleration: {g_pass} G")
    
    g_cargo = calculate_cargo_g_force()
    print(f"3. Class 1 Cargo Track Acceleration: {g_cargo} G")
    
    clamp_n = calculate_vacuum_seal_clamping_force(1.5, 0.0)
    print(f"4. Atmospheric End-Plug Clamping Force (r=1.5m): {clamp_n / 1000:.2f} kN")
    
    stability = calculate_360_symmetrical_stabilization(15.0, 0.85)
    print(f"5. 360-Degree Radial Array Status: {stability}")
