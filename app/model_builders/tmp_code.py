
    def _create_pa_mastermix(self):
        water=ConcreteReagent.objects.get(name='DNA Free Water')
        buffer_mix=MixedReagent.make(
            self._create_pa_buffermix(), Concentration.make(3.3, 1, 'X'))
        primers=PlaceholderReagent.make('Primers', 
            Concentration.make(10, 0.4, 'uM each'))
        hgDNA=PlaceholderReagent.make('HgDNA', 
            Concentration.make(120, 60, 'ng/ul'))
        template=PlaceholderReagent.make('Template', 
            Concentration.make(1, 0.1, 'cp/ul'))
        final_volume=50

        mastermix = MasterMix.make(
            water, buffer_mix, primers, hgDNA, template, final_volume)
        return mastermix

    def _create_id_mastermix(self):
        water=ConcreteReagent.objects.get(name='DNA Free Water')
        buffer_mix=MixedReagent.make(
            self._create_id_buffermix(), Concentration.make(2.0, 1, 'X'))
        primers=PlaceholderReagent.make('Primers', 
            Concentration.make(10, 0.4, 'uM each'))
        hgDNA=None
        template=PlaceholderReagent.make('Template', 
            Concentration.make(10, 2.5, 'cp/ul'))
        final_volume=20

        mastermix = MasterMix.make(
            water, buffer_mix, primers, hgDNA, template, final_volume)
        return mastermix

    def _create_pa_buffermix(self):
        buffermix = BufferMix.objects.create(
            volume=15,
            final_volume=50,
        )
        for name in ('DNA Free Water', 'Titanium PCR Buffer', 'KCl', 'MgCl2',
                'BSA', 'dNTPs'):
            reagent = ConcreteReagent.objects.get(name=name)
            buffermix.concrete_reagents.add(reagent)
        # Taq requires additional disambiguation.
        taq = ConcreteReagent.objects.get(
            name='Titanium Taq', concentration__final=1.00)
        buffermix.concrete_reagents.add(taq)

        buffermix.save()
        return buffermix

    def _create_id_buffermix(self):
        buffermix = BufferMix.objects.create(
            volume=10,
            final_volume=20,
        )
        for name in ('DNA Free Water', 'KCl', 'MgCl2', 'BSA', 
                'Triton', 'SYBRgreen', 'dNTPs', 'KOH'):
            reagent = ConcreteReagent.objects.get(name=name)
            buffermix.concrete_reagents.add(reagent)
        # Taq requires additional disambiguation.
        taq = ConcreteReagent.objects.get(
            name='Titanium Taq', concentration__final=1.3)
        buffermix.concrete_reagents.add(taq)

        buffermix.save()
        return buffermix


    def _create_primer_kit(self):
        return PrimerKit.make(
            self._make_pa_primers(),
            self._make_id_primers(),
            Concentration.make(10, 0.4, 'uM'),
            Concentration.make(10, 0.4, 'uM'),
        )

    def _create_strain_kit(self):
        strains = [Strain.objects.get(name=name) for name in (
            'ATCC 15764',
            'ATCC 15764',
            'ATCC 26189',
            'ATCC 700802',
            'ATCC BAA-1705',
            'ATCC BAA-2317',
            'ATCC BAA-2355',
            'ATCC BAA-633',
            'ATCC BAA-633'
        )]
        return StrainKit.make(strains)
