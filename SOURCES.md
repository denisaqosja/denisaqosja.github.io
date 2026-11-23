# Content sources and figure notes

## Profile and background

- The About text, professional headline, and four technical skill categories are supplied by the user in the November 23, 2026 revisions. Paragraph breaks are added to the About text for readability.

- The user’s local English CV, `ResumeDenisaQosja.pdf` (March 2026): work history, degree titles, thesis title, and skills. The original PDF is not copied into the published site.
- [Public ORCID record](https://orcid.org/0000-0003-3083-8253): cross-check of employment, education, and publication identity.
- [Google Scholar profile supplied by the user](https://scholar.google.com/citations?user=yeD9RRkAAAAJ&hl=en): linked directly. Automated access was rate-limited, so publication content was verified through the papers, DOI records, and local bibliography instead. No citation counts were inferred.
- Portrait: user’s local professional CV photograph, resized and cropped for the site.

## Publications

- [Enhancing Fourier-based Doppler Resolution with Diffusion Models](https://arxiv.org/abs/2505.17567), IRS 2025. [Full paper](https://arxiv.org/html/2505.17567v1). The summary includes simulated-data scope and the reported hallucination failure case.
- [SAR Image Synthesis with Diffusion Models](https://arxiv.org/abs/2405.07776), RadarConf 2024. [Full paper](https://arxiv.org/html/2405.07776v1). The FID chart uses conditional model scores from Table I and the pretrained conditional DDPM score from Table II. These are paper-reported values, not a new benchmark.
- [Small Target Detection in a Radar Surveillance System Using Contractive Autoencoders](https://doi.org/10.1109/TAES.2023.3253469). The journal issue is 60(1), pages 51–67, February 2024; early access was 2023. This distinction is explicitly retained in the website.
- [Benchmarking Convolutional Neural Network Backbones for Target Classification in SAR](https://doi.org/10.1109/RadarConf2351548.2023.10149802), RadarConf 2023. Authors and venue were also checked against the [coauthor’s university publication list](https://etit.ruhr-uni-bochum.de/en/est/team/prof-dr-ing-stefan-brueggenwirth/).

Website abstracts are original concise summaries, not verbatim reproductions. Each entry links to the original publication.

## Projects

- [ComplexValuedNN](https://github.com/denisaqosja/ComplexValuedNN): README and [Results.md](https://github.com/denisaqosja/ComplexValuedNN/blob/main/Results.md). This is the repository corresponding to the user’s “complex-valuedNN” description. No numerical performance claim is made on the website.
- [Sentinel_SEN12MS_Segmentation](https://github.com/denisaqosja/Sentinel_SEN12MS_Segmentation): repository verified from the local checkout’s Git remote and public README. Local README and code structure inform the DINOv3/SegFormer description. Full SEN12MS inference is described as a goal; dataset masks are not represented as predictions.
- [RadarSignalProcessing](https://github.com/denisaqosja/RadarSignalProcessing): public README, processing chain, and configuration overview.

Project-to-publication links indicate related research, not a claim that a repository is the official implementation of a paper.

## Assets

- `sentinel-ground-truth.jpg`: resized from the local Sentinel project’s `resources/docs/figures/dfc_samples_masks.png`. Contains actual DFC2020 dataset image/annotation pairs and its class-color legend. Source figure generation lives in that project. The caption identifies ground truth explicitly.
- `sar-fid.svg`: newly drawn chart of published results, cited above.
- `doppler.svg`, `complex-network.svg`, `radar-pipeline.svg`, `detection.svg`, and `classification.svg`: original conceptual illustrations, not measured data or model outputs.
- The Doppler slider draws an analytical normalized sinc-squared response, for explanation only. It does not execute a network or the repository.

## Design references

- [Angel Villar-Corrales’s homepage](https://angelvillarcorrales.com/), inspected from its live HTML and stylesheet on November 23, 2026: compact biography, portrait beside the profile, restrained typography, and publication rows.
- [Ilyes Jaouedi’s portfolio](https://ilyes-jaouedi.github.io/), inspected from its live HTML and stylesheet on November 23, 2026: compact top navigation, an initials brand, title-case navigation links, and a mobile menu.
- [Mario Qosja’s homepage](https://qosmar.github.io/) informed an earlier header revision. The current design follows the newer references above.

All site markup and CSS are independently implemented. The references’ biographical text and research content are not included.
