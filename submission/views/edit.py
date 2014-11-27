from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from submission.forms import SubmissionForm
from submission.forms import SubmissionFileForm
from submission.models import Submission

@login_required
def edit(request, submission_id):
    if request.user.has_perm('submission.review'):
        instance = get_object_or_404(Submission, id=submission_id)
    else:
        instance = get_object_or_404(Submission, id=submission_id, user=request.user)

    if request.POST.get('submit'):
        if request.FILES:
            submission = SubmissionForm(request.POST, request.FILES, instance=instance)
        else:
            submission = SubmissionForm(request.POST, instance=instance)

        if submission.is_valid():

            sub = submission.save()

            if request.FILES.getlist('slide'):

                for f in sub.files.all():
                    f.file.delete()
                    f.delete()

                for f in request.FILES.getlist('slide'):
                    form = SubmissionFileForm().save(commit=False)
                    form.submission = sub
                    form.file = f
                    form.save()

            return redirect('submission:list')
        else:
            pass

    context = {
            'user': request.user,
            'rule': render_document(Node(nid=settings.SUBMISSION_RULE_DOCID).model.current_revision.text.text),
            'submission': instance,
            }

    return render(request, 'submission/edit.html', context)
