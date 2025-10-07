#!/usr/bin/env python3
"""
tdc_monte_carlo.py - Universal Monte Carlo framework for TDC simulations
Features:
- Parameter sampling with different distributions and reproducible seeding
- TDC-specific cost calculations (Landauer, phase transitions, entropy production)
- Cross-validation with baseline models
- Statistical significance testing with detailed logging
- Domain-specific examples for all TDC use cases
"""
import numpy as np
from typing import Callable, Dict, List, Tuple, Optional
import scipy.stats as stats
from dataclasses import dataclass
import logging
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# Physical constants
K_B = 1.380649e-23 # Boltzmann constant (J/K)
@dataclass
class TDCParameter:
    """Parameter specification for Monte Carlo sampling"""
    name: str
    distribution: str # 'uniform', 'normal', 'lognormal'
    bounds: Tuple[float, float] # (min, max) for uniform, (mean, std) for normal
    description: str = ""
class TDCMonteCarlo:
    """
    Universal Monte Carlo framework for TDC simulations across domains
    """
   
    def __init__(self, confidence_level: float = 0.95):
        self.confidence_level = confidence_level
        self.failed_trials = [] # Track failed trials for debugging
       
    def sample_parameters(self, param_specs: Dict[str, TDCParameter], n_samples: int,
                         seed: Optional[int] = None) -> List[Dict]:
        """Sample parameters according to specified distributions with optional seeding"""
        if seed is not None:
            np.random.seed(seed)
            logger.info(f"Using random seed: {seed} for reproducible sampling")
       
        samples = []
       
        for i in range(n_samples):
            sample = {}
            for param_name, param_spec in param_specs.items():
                if param_spec.distribution == 'uniform':
                    sample[param_name] = np.random.uniform(*param_spec.bounds)
                elif param_spec.distribution == 'normal':
                    sample[param_name] = np.random.normal(*param_spec.bounds)
                elif param_spec.distribution == 'lognormal':
                    sample[param_name] = np.random.lognormal(*param_spec.bounds)
            samples.append(sample)
           
        logger.info(f"Generated {n_samples} parameter samples")
        return samples
   
    def calculate_tdc_cost(self, results: Dict, params: Dict) -> Dict[str, float]:
        """
        Calculate TDC-specific costs:
        - Landauer cost (information erasure)
        - Phase transition cost (soliton formation)
        - Entropy production cost (non-equilibrium processes)
        """
        # Extract relevant parameters
        S_star = params.get('S', 0.2) / (K_B * params.get('T', 310))
        Dr = params.get('Dr', 3.0)
        r_mean = np.mean(results.get('residue', [0.1]))
        epsilon = params.get('epsilon', 0.1)
       
        # 1. Landauer cost (information erasure)
        erased_bits = max(0, (1 - 1/Dr) * r_mean) # Proxy for information loss
        landauer_cost = K_B * params.get('T', 310) * np.log(2) * erased_bits
       
        # 2. Phase transition cost (soliton formation)
        chi_threshold = params.get('chi_threshold', 0.5)
        phase_cost = epsilon * abs(r_mean) if S_star > chi_threshold else 0
       
        # 3. Entropy production (non-equilibrium cost)
        # Estimate from signal variability or use actual entropy if available
        if 'eet_efficiency' in results:
            signal_var = np.var(results['eet_efficiency'])
        elif 'signal' in results:
            signal_var = np.var(results['signal'])
        else:
            signal_var = 0.1 # Default
           
        entropy_cost = K_B * params.get('T', 310) * signal_var
       
        total_cost = landauer_cost + phase_cost + entropy_cost
       
        return {
            'landauer_cost': landauer_cost,
            'phase_cost': phase_cost,
            'entropy_cost': entropy_cost,
            'total_cost': total_cost,
            'efficiency_cost_ratio': total_cost / (r_mean + 1e-6) # Normalized
        }
   
    def extract_primary_metric(self, results: Dict, domain: str) -> float:
        """Extract domain-specific primary performance metric"""
        if domain == 'geo_bio':
            return np.mean(results.get('eet_efficiency', [0]))
        elif domain == 'neural':
            signals = results.get('normalized_signals', {})
            if signals and len(signals) > 1:
                corrs = [np.corrcoef(s1, s2)[0,1] for s1, s2 in zip(signals.values(), list(signals.values())[1:])]
                return np.mean(corrs) if corrs else 0.0
            return 0.0
        elif domain == 'gut_brain':
            return np.mean(results.get('snr', [0]))
        else:
            # Default: try common metrics
            for metric in ['eet_efficiency', 'snr', 'correlation', 'soc_exponent']:
                if metric in results:
                    values = results[metric]
                    if hasattr(values, '__len__') and len(values) > 0:
                        return np.mean(values)
                    elif isinstance(values, (int, float)):
                        return float(values)
            return 0.0
   
    def run_analysis(
        self,
        sim_func: Callable,
        base_params: Dict,
        param_specs: Dict[str, TDCParameter],
        domain: str,
        n_trials: int = 100,
        baseline_func: Optional[Callable] = None,
        seed: Optional[int] = None
    ) -> Dict:
        """
        Run comprehensive Monte Carlo analysis
       
        Args:
            sim_func: TDC simulation function
            base_params: Fixed parameters for simulation
            param_specs: Parameters to vary with distributions
            domain: Domain name for metric extraction
            n_trials: Number of Monte Carlo trials
            baseline_func: Optional baseline model for comparison
            seed: Random seed for reproducible sampling
        """
        logger.info(f"Starting TDC Monte Carlo analysis for {domain} domain")
        logger.info(f"Parameters varied: {list(param_specs.keys())}")
        logger.info(f"Number of trials: {n_trials}")
       
        # Reset failed trials tracking
        self.failed_trials = []
       
        # Sample parameters
        param_samples = self.sample_parameters(param_specs, n_trials, seed)
       
        # Run simulations
        metrics = []
        costs = []
        baseline_metrics = []
       
        for i, sample_params in enumerate(param_samples):
            if i % 10 == 0:
                logger.info(f"Progress: {i}/{n_trials} trials")
               
            # Combine base and sampled parameters
            full_params = {**base_params, **sample_params}
          
            # ==================================================================
            # Run TDC simulation
            # ==================================================================
            try:
                results = sim_func(**full_params)
               
                # Extract metrics
                primary_metric = self.extract_primary_metric(results, domain)
                cost_metrics = self.calculate_tdc_cost(results, full_params)
               
                metrics.append(primary_metric)
                costs.append(cost_metrics)
               
                # Run baseline if provided
                if baseline_func:
                    try:
                        baseline_results = baseline_func(**full_params)
                        baseline_metric = self.extract_primary_metric(baseline_results, domain)
                        baseline_metrics.append(baseline_metric)
                    except Exception as e:
                        logger.warning(f"Baseline trial {i} failed: {e}")
                        baseline_metrics.append(0.0)
                       
            except Exception as e:
                logger.warning(f"Trial {i} failed: {e}")
                self.failed_trials.append({
                    'trial_index': i,
                    'parameters': full_params,
                    'error': str(e)
                })
                metrics.append(0.0)
                costs.append({'total_cost': 0.0, 'efficiency_cost_ratio': 0.0})
                if baseline_func:
                    baseline_metrics.append(0.0)
                  
        # ==================================================================
        # Statistical analysis
        # ==================================================================
        analysis = self._compute_statistics(metrics, costs, baseline_metrics)
        analysis['domain'] = domain
        analysis['n_successful_trials'] = len([m for m in metrics if m > 0])
        analysis['failed_trials'] = self.failed_trials
       
        logger.info(f"Analysis complete: {analysis['n_successful_trials']}/{n_trials} successful trials")
       
        return analysis
   
    def _compute_statistics(self, metrics: List[float], costs: List[Dict],
                          baseline_metrics: List[float]) -> Dict:
        """Compute comprehensive statistics with detailed failure logging"""
        # Filter out failed trials (metrics <= 0)
        valid_indices = [i for i, m in enumerate(metrics) if m > 0]
        valid_metrics = [metrics[i] for i in valid_indices]
        valid_costs = [costs[i] for i in valid_indices]
       
        if not valid_metrics:
            logger.error("No successful trials - all metrics are zero or negative")
            return {'error': 'No successful trials', 'failed_count': len(metrics)}
       
        failure_rate = (len(metrics) - len(valid_metrics)) / len(metrics)
        logger.info(f"Trial success rate: {len(valid_metrics)}/{len(metrics)} ({1-failure_rate:.1%})")
       
        if failure_rate > 0.5:
            logger.warning(f"High failure rate: {failure_rate:.1%} - check parameter ranges")

        # ==================================================================
        # Basic statistics
        # ==================================================================
        stats_dict = {
            'primary_metric': {
                'mean': np.mean(valid_metrics),
                'std': np.std(valid_metrics),
                'ci_low': np.percentile(valid_metrics, (1-self.confidence_level)/2 * 100),
                'ci_high': np.percentile(valid_metrics, (1+self.confidence_level)/2 * 100),
                'min': np.min(valid_metrics),
                'max': np.max(valid_metrics),
                'n_valid': len(valid_metrics)
            },
            'failure_rate': failure_rate
        }
        
        # ==================================================================                  
        # Cost statistics
        # ==================================================================
        cost_keys = valid_costs[0].keys() if valid_costs else []
        for key in cost_keys:
            values = [c[key] for c in valid_costs]
            stats_dict[f'cost_{key}'] = {
                'mean': np.mean(values),
                'std': np.std(values),
                'min': np.min(values),
                'max': np.max(values)
            }
      
        # ==================================================================
        # Baseline comparison
        # ==================================================================
        if baseline_metrics:
            valid_baseline_indices = [i for i, m in enumerate(baseline_metrics) if m > 0]
            valid_baseline = [baseline_metrics[i] for i in valid_baseline_indices]
           
            if valid_baseline:
                # Ensure we compare the same trials
                common_indices = set(valid_indices) & set(valid_baseline_indices)
                if common_indices:
                    tdc_comparison = [metrics[i] for i in common_indices]
                    baseline_comparison = [baseline_metrics[i] for i in common_indices]
                   
                    t_stat, p_value = stats.ttest_rel(tdc_comparison, baseline_comparison)
                    improvement = (np.mean(tdc_comparison) - np.mean(baseline_comparison)) / np.mean(baseline_comparison)
                   
                    stats_dict['baseline_comparison'] = {
                        'tdc_mean': np.mean(tdc_comparison),
                        'baseline_mean': np.mean(baseline_comparison),
                        'improvement': improvement,
                        'p_value': p_value,
                        'significant': p_value < 0.05,
                        'n_comparison_trials': len(common_indices)
                    }
                else:
                    logger.warning("No common successful trials for baseline comparison")
       
        return stats_dict
   
    def print_report(self, analysis: Dict):
        """Print comprehensive Monte Carlo report"""
        print("\n" + "="*60)
        print("TDC MONTE CARLO ANALYSIS REPORT")
        print("="*60)
        print(f"Domain: {analysis.get('domain', 'Unknown')}")
        print(f"Successful trials: {analysis.get('n_successful_trials', 0)}")
        print(f"Failure rate: {analysis.get('failure_rate', 0):.1%}")
       
        if 'primary_metric' in analysis:
            pm = analysis['primary_metric']
            print(f"\nPrimary Metric:")
            print(f" Mean: {pm['mean']:.4f} ± {pm['std']:.4f}")
            print(f" 95% CI: [{pm['ci_low']:.4f}, {pm['ci_high']:.4f}]")
            print(f" Range: [{pm['min']:.4f}, {pm['max']:.4f}]")
            print(f" Valid trials: {pm['n_valid']}")
       
        if 'baseline_comparison' in analysis:
            bc = analysis['baseline_comparison']
            print(f"\nBaseline Comparison:")
            print(f" TDC: {bc['tdc_mean']:.4f}")
            print(f" Baseline: {bc['baseline_mean']:.4f}")
            print(f" Improvement: {bc['improvement']:+.2%}")
            print(f" Statistical significance: {'YES' if bc['significant'] else 'NO'} (p={bc['p_value']:.4f})")
            print(f" Comparison trials: {bc['n_comparison_trials']}")
       
        # Print cost metrics
        cost_metrics = {k: v for k, v in analysis.items() if k.startswith('cost_')}
        if cost_metrics:
            print(f"\nCost Analysis:")
            for cost_name, cost_stats in cost_metrics.items():
                print(f" {cost_name}: {cost_stats['mean']:.2e} ± {cost_stats['std']:.2e}")
       
        # Print failed trials summary
        failed_trials = analysis.get('failed_trials', [])
        if failed_trials:
            print(f"\nFailed Trials Summary: {len(failed_trials)} failures")
            for i, failure in enumerate(failed_trials[:3]): # Show first 3
                print(f" Trial {failure['trial_index']}: {failure['error']}")
            if len(failed_trials) > 3:
                print(f" ... and {len(failed_trials) - 3} more failures")

# ==================================================================
# Example usage function with switchable domain
# ==================================================================
def example_usage(domain: str = 'geo_bio'):
    """Switchable example usage for TDC domains
    Demonstrates configuration for different domains - adapt for your simulations
    
    Args:
        domain: 'geo_bio', 'neural', or 'gut_brain' (or add new)
    """
    print(f"=== {domain.capitalize().replace('_', '-')} Domain Example ===")
   
    # Domain-specific configurations (switchable)
    if domain == 'geo_bio':
        param_specs = {
            'Dr': TDCParameter('Dr', 'uniform', (2.0, 4.0), 'Drift ratio for criticality tuning'),
            'S': TDCParameter('S', 'uniform', (0.1, 0.3), 'Entropy parameter for flux variability'),
            'r0': TDCParameter('r0', 'normal', (0.3, 0.1), 'Initial mineral mat residue'),
        }
        base_params = {
            'temp_grad': 50,
            'pot_grad': 0.1,
            'pressure': 350,
            'T': 573,
            'epsilon': 0.1,
            'chi_threshold': 0.5
        }
        # sim_func = your_geo_bio_sim  # e.g. from tdc_eg3
       
    elif domain == 'neural':
        param_specs = {
            'Dr': TDCParameter('Dr', 'uniform', (2.5, 3.5), 'Drift ratio for universality'),
            'S': TDCParameter('S', 'uniform', (0.15, 0.25), 'Entropy for signal variability'),
            'I': TDCParameter('I', 'normal', (1.0, 0.2), 'Inertia parameter'),
        }
        base_params = {
            'domains': ['neural', 'bacterial', 'geological'],
            'T': 310,
        }
        # sim_func = your_neural_sim  # e.g. from tdc_eg1
       
    elif domain == 'gut_brain':
        param_specs = {
            'Dr': TDCParameter('Dr', 'uniform', (0.1, 0.3), 'Drift ratio for gut-brain coupling'),
            'S': TDCParameter('S', 'uniform', (0.18, 0.25), 'Entropy for transduction'),
            'alpha': TDCParameter('alpha', 'uniform', (0.005, 0.02), 'Residue decay rate'),
        }
        base_params = {
            'temp_grad': 50,
            'pot_grad': 0.1,
            'T': 310,
        }
        # sim_func = your_gut_brain_sim  # e.g. from tdc_eg2
       
    else:
        raise ValueError(f"Unknown domain: {domain}. Add config or use custom.")
   
    print(f"Configured for {domain} - uncomment sim_func and run_analysis to execute")
    print(f"Parameters to vary: {list(param_specs.keys())}")
    print(f"Base parameters: {base_params}")
    
    # ==================================================================
    # In practice:
    # ==================================================================
    # mc = TDCMonteCarlo()
    # analysis = mc.run_analysis(sim_func, base_params, param_specs, domain, n_trials=50, seed=42)
    # mc.print_report(analysis)
if __name__ == "__main__":
    # Demonstrate with different domains
    example_usage('geo_bio')
    print("\n")
    example_usage('neural')
    print("\n")
    example_usage('gut_brain')
   
    print("\n" + "="*60)
    print("To use: Import TDCMonteCarlo and call run_analysis() with your simulation function")
    print("Use example_usage(domain) as template - add new domains by extending the switch")"
