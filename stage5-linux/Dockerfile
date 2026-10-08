FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    openssh-server \
    sudo \
    && mkdir /var/run/sshd

RUN useradd -m -s /bin/bash investigator && echo 'investigator:investigator123' | chpasswd
RUN useradd -m -s /bin/bash lizard && echo 'lizard:lizard123' | chpasswd

RUN groupadd legacy_proj && usermod -aG legacy_proj lizard

RUN mkdir -p /srv/onboarding_evidence
RUN echo 'FLAG{stale_gr0up_m3mb3rsh1p}' > /srv/onboarding_evidence/rabbit_id.txt
RUN chown root:legacy_proj /srv/onboarding_evidence/rabbit_id.txt
RUN chmod 640 /srv/onboarding_evidence/rabbit_id.txt
RUN chown root:legacy_proj /srv/onboarding_evidence
RUN chmod 750 /srv/onboarding_evidence

RUN echo 'investigator ALL=(lizard) NOPASSWD: ALL' > /etc/sudoers.d/investigator
RUN chmod 440 /etc/sudoers.d/investigator

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]